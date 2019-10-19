import sys

if 'pandas' in sys.modules.keys():
    from dovpanda.core import ledger
    ledger.register_hooks()
else:
    print('Pandas not imported')
