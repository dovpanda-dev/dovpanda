from dovpanda import base
from dovpanda.base import Ledger

ledger = Ledger()


@ledger.add_hint('DataFrame.__init__')
def init_for_checks(*args, **kwargs):
    ledger.tell('you have construted a df')


@ledger.add_hint('DataFrame.__init__')
def init_another(*args, **kwargs):
    ledger.tell('another pre hook for init')


@ledger.add_hint('DataFrame.iterrows')
def iterrows_is_bad(*args, **kwargs):
    ledger.tell("iterrows is not recommended, and in the majority of cases will have better alternatives")


@ledger.add_hint('DataFrame.groupby')
def time_grouping(*args, **kwargs):
    try:
        by = args[1]
    except IndexError:
        by = kwargs.get('by')
    base.listify(by)
    if 'hour' in by:
        ledger.tell('Seems like you are grouping by time, consider using resample')


@ledger.add_hint('concat', hook_type='post')
def duplicate_index_after_concat(res, *args, **kwargs):
    if res.index.nunique() != len(res.index):
        ledger.tell('After concatenation you have duplicated indexes values - pay attention')
    if res.columns.nunique() != len(res.columns):
        ledger.tell('After concatenation you have duplicated column names - pay attention')


@ledger.add_hint('concat')
def concat_single_column(*args, **kwargs):
    objs = base.get_arg(args, kwargs, 0, 'objs')
    axis = base.get_arg(args, kwargs, 1, 'axis')
    cols = {df.shape[1] for df in objs}
    if axis == 1 and 1 in cols:
        ledger.tell(
            'One of the dataframes you are concatenating is with a single column, '
            'consider using `df.assign()` or `df.insert()`')


@ledger.add_hint('concat')
def wrong_concat_axis(*args, **kwargs):
    objs = base.get_arg(args, kwargs, 0, 'objs')
    axis = base.get_arg(args, kwargs, 1, 'axis')
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
def df_check_equality(*args):
    if type(args[0]) == type(args[1]):
        ledger.tell(f'Calling df1 == df2 compares the objects element-wise. '
                    'If you need a boolean condition, try df1.equals(df2)')


@ledger.add_hint('Series.__eq__')
def series_check_equality(*args):
    if type(args[0]) == type(args[1]):
        ledger.tell(f'Calling series1 == series2 compares the objects element-wise. '
                    'If you need a boolean condition, try series1.equals(series2)')


@ledger.add_hint('read_csv','post')
def csv_index(res, *args, **kwargs):
    filename = base.get_arg(args,kwargs,0,'filepath_or_buffer')
    if type(filename) is str:
        filename = "'" + filename + "'"
    else:
        filename = 'file'
    if 'Unnamed: 0' in res.columns:
        if (len(args) < 5) and ('index_col' not in kwargs.keys()):
            ledger.tell('Your left most column is unnamed. This suggets it might be the index column, try: '
                        f'<code>pd.read_csv({filename}, index_col=0)</code>')


