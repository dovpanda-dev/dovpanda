import sys

from dovpanda.core import ledger
if 'pandas' in sys.modules.keys():
    ledger.register_hints()
else:
    ledger.tell('Pandas not imported')

def set_output(tell_method):
    ledger.set_output(tell_method)