import pandas as pd

READ_METHODS = [method for method in dir(pd) if 'read' in method]
DF_CREATION = READ_METHODS + ['DataFrame']
SERIES_CREATION = READ_METHODS + ['Series.__init__']
GET_ITEM = ['DataFrame.__getitem__', 'Series.__getitem__',
            'core.indexing._NDFrameIndexer.__getitem__', 'core.indexing._LocationIndexer.__getitem__']

TIME_COLUMNS = ['year', 'month', 'week', 'day', 'hour', 'minute', 'second', 'weekday', 'time']
# Translation dict
ndim_to_obj = {1: 'series', 2: 'df'}

#
CATEGORY_SHARE_THRESHOLD = 4

MAX_CSV_SIZE = 100000000  # Size in bytes, 100 MB
