import pandas as pd

READ_METHODS = [method for method in dir(pd) if 'read' in method]
DF_CREATION = READ_METHODS + ['DataFrame']
SERIES_CREATION = READ_METHODS + ['Series.__init__']

#
CATEGORY_SHARE_THRESHOLD = 4
MAX_CSV_SIZE = 10000000  # Size in bytes, 10 MB
