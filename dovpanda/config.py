import inspect
import pathlib

import pandas

# Dirs
PANDAS_DIR = pathlib.Path(inspect.getsourcefile(pandas)).parent.absolute()
CURDIR = pathlib.Path(inspect.getsourcefile(inspect.currentframe())).parent.absolute()
RESTRICTED_DIRS = [PANDAS_DIR, CURDIR]


def is_callable(obj):
    return inspect.ismethod(obj) or inspect.isfunction(obj)


def get_callables(obj):
    return inspect.getmembers(obj, predicate=is_callable)


def methods_by_argument(arg_name):
    ret = []
    for obj in [pandas.DataFrame, pandas.Series]:
        for name, func in inspect.getmembers(obj, is_callable):
            if name.startswith('_'):
                continue
            signature = inspect.signature(func)
            if arg_name in signature.parameters.keys():
                ret.append(f'{obj.__name__}.{name}')
    return ret


# pandas mathods
PD_ALL = [f[0] for f in get_callables(pandas)]
DF_ALL = ['DataFrame.' + f[0] for f in get_callables(pandas.DataFrame)]
SERIES_ALL = ['Series.' + f[0] for f in get_callables(pandas.Series)]

READ_METHODS = [method for method in PD_ALL if 'read' in method]
WRITE_TEXT_METHODS = ['DataFrame.to_csv', 'DataFrame.to_json', 'Series.to_csv', 'Series.to_json']
DF_CREATION = READ_METHODS
SERIES_CREATION = READ_METHODS + ['Series.__init__']
GET_ITEM = ['DataFrame.__getitem__', 'Series.__getitem__',
            'core.indexing._NDFrameIndexer.__getitem__', 'core.indexing._LocationIndexer.__getitem__']
MERGE_DFS = ['merge', 'merge_ordered', 'merge_asof', 'concat', 'DataFrame.append', 'DataFrame.join']

# lists
TIME_COLUMNS = ['year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'weekday', 'time']

# Translation dict

ndim_to_obj = {1: 'series', 2: 'df'}
color_to_level = {'blue': 'info', 'red': 'danger', 'green': 'success', 'yellow': 'warning',
                  'brightblue': 'primary', 'grey': 'secondary', 'white': 'light', 'black': 'dark'}
#
CATEGORY_SHARE_THRESHOLD = 4

MAX_CSV_SIZE = 100000000  # Size in bytes, 100 MB

try:
    with (CURDIR / 'resource' / 'logo').open('r') as f:
        logo = f.read()
    logo_tag = f'<img src="{logo}" alt="logo" style="float:left; margin-right:10px">'
except FileNotFoundError:
    logo = None
    logo_tag = ''

# HTMLs
html_bug = '''
<h1 style="color: black; margin-top: 0">SAD PANDA</h1><br>
I'm so sorry, but I crashed on <code>{hint}</code> with error <code>{e}</code><br>
<strong>But you can change that!</strong><br>
Please
<a href="https://github.com/dovpanda-dev/dovpanda/issues/new?assignees=&labels=bug&template=bug_report.md&title=">
    Report a bug
</a>
'''

html_tell = '''
<div class="alert alert-{level}" role="alert">
  {logo_tag}
  {message}
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
  <div style="font-size:0.7em;">
    Line {lineno}: <code>{code_context}</code>
  </div>

</div>
'''
