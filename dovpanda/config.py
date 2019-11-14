import inspect
import pathlib

import pandas

# Dirs
PANDAS_DIR = pathlib.Path(inspect.getsourcefile(pandas)).parent.absolute()
CURDIR = pathlib.Path(inspect.getsourcefile(inspect.currentframe())).parent.absolute()
z = inspect.getsourcefile(inspect.currentframe())
RESTRICTED_DIRS = [PANDAS_DIR, CURDIR]
# pandas mathods
READ_METHODS = [method for method in dir(pandas) if 'read' in method]
DF_CREATION = READ_METHODS + ['DataFrame']
SERIES_CREATION = READ_METHODS + ['Series.__init__']
GET_ITEM = ['DataFrame.__getitem__', 'Series.__getitem__',
            'core.indexing._NDFrameIndexer.__getitem__', 'core.indexing._LocationIndexer.__getitem__']

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
