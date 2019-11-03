import numpy as np
from dateutil.parser import parse

from dovpanda import base, config
from dovpanda.base import Ledger

ledger = Ledger()


@ledger.add_hint('DataFrame.iterrows')
def iterrows_is_bad(arguments):
    ledger.tell("iterrows is not recommended, and in the majority of cases will have better alternatives")


@ledger.add_hint('DataFrame.groupby')
def time_grouping(arguments):
    by = arguments.get('by')
    base.listify(by)
    if 'hour' in by:
        ledger.tell('Seems like you are grouping by time, consider using resample')


@ledger.add_hint('concat', hook_type='post')
def duplicate_index_after_concat(res, arguments):
    if res.index.nunique() != len(res.index):
        ledger.tell('After concatenation you have duplicated indexes values - pay attention')
    if res.columns.nunique() != len(res.columns):
        ledger.tell('After concatenation you have duplicated column names - pay attention')


@ledger.add_hint('concat')
def concat_single_column(arguments):
    objs = arguments.get('objs')
    axis = arguments.get('axis')
    cols = {df.shape[1] for df in objs}
    if axis == 1 and 1 in cols:
        ledger.tell(
            'One of the dataframes you are concatenating is with a single column, '
            'consider using `df.assign()` or `df.insert()`')


@ledger.add_hint('concat')
def wrong_concat_axis(arguments):
    objs = arguments.get('objs')
    axis = arguments.get('axis')
    rows = {df.shape[0] for df in objs}
    cols = {df.shape[1] for df in objs}
    col_names = set.union(*[set(df.columns) for df in objs])
    same_cols = (len(cols) == 1) and (len(col_names) == list(cols)[0])
    same_rows = (len(rows) == 1)
    axis_translation = {0: 'vertically', 1: 'horizontally'}
    if same_cols and not same_rows:
        if axis == 1:
            ledger.tell("All dataframes have the same columns, which hints for concat on axis 0."
                        "You specified <code>axis=1</code> which may result in an unwanted behaviour")
    elif same_rows and not same_cols:
        if axis == 0:
            ledger.tell("All dataframes have same number of rows, which hints for concat on axis 1."
                        "You specified <code>axis=0</code> which may result in an unwanted behaviour")

    elif same_rows and same_rows:
        ledger.tell("All dataframes have the same columns and same number of rows. "
                    f"Pay attention, your axis is {axis} which concatenates {axis_translation[axis]}")


@ledger.add_hint('DataFrame.__eq__')
def df_check_equality(arguments):
    print(arguments)
    if isinstance(arguments.get('self'), type(arguments.get('other'))):
        ledger.tell(f'Calling df1 == df2 compares the objects element-wise. '
                    'If you need a boolean condition, try df1.equals(df2)')


@ledger.add_hint('Series.__eq__')
def series_check_equality(arguments):
    if isinstance(arguments.get('self'), type(arguments.get('other'))):
        ledger.tell(f'Calling series1 == series2 compares the objects element-wise. '
                    'If you need a boolean condition, try series1.equals(series2)')


@ledger.add_hint('read_csv', 'post')
def csv_index(res, arguments):
    filename = arguments.get('filepath_or_buffer')
    if type(filename) is str:
        filename = "'" + filename + "'"
    else:
        filename = 'file'
    if 'Unnamed: 0' in res.columns:
        if arguments.get('index_col') is None:
            ledger.tell('Your left most column is unnamed. This suggets it might be the index column, try: '
                        f'<code>pd.read_csv({filename}, index_col=0)</code>')


@ledger.add_hint(config.DF_CREATION, 'post')
def suggest_category_dtype(res, arguments):
    rows = res.shape[0]
    threshold = int(rows / config.CATEGORY_SHARE_THRESHOLD) + 1
    obj_type = (res.select_dtypes('object')
                .nunique()
                .loc[lambda x: x <= threshold]
                .to_dict())
    for col, uniques in obj_type.items():
        if uniques == 2:
            dtype = 'boolean'
            arbitrary = res.loc[:, col].at[0]
            code = f"df['{col}'] = (df['{col}'] == '{arbitrary}')"
        else:
            dtype = 'categorical'
            code = f"df['{col}'] = df['{col}'].astype('category')"
        message = (f"Dataframe has {rows} rows. Column <code>{col}</code> has only {uniques} values "
                   f"which suggests it's a {dtype} feature.<br>"
                   f"After df is created, Consider converting it to {dtype} by using "
                   f"<code>{code}</code>")
        ledger.tell(message)


@ledger.add_hint('DataFrame.insert')
def data_in_date_format_insert(arguments):
    column_name = arguments.get('column')
    value = arguments.get('value')

    value_array = np.asarray(value)

    # check if exception rasied when trying to parse content
    try:
        list(map(parse, value_array))
    except ValueError:
        return
    except TypeError:
        return

    if not np.issubdtype(value_array.dtype, np.datetime64):
        # if there was no exception the content in a datetime format but not in datetime type
        ledger.tell(
            "You entered value in a struct of datetime but the type is somthing different. "
            f"Try using <code>pd.to_datetime(df.{column_name})</code>")
