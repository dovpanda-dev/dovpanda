import pandas as pd

READ_METHODS = [method for method in dir(pd) if 'read' in method]
DF_CREATION = READ_METHODS + ['DataFrame']
SERIES_CREATION = READ_METHODS + ['Series.__init__']

#
CATEGORY_SHARE_THRESHOLD = 4
