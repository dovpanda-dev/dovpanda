import sys

from dovpanda.core import ledger
if 'pandas' in sys.modules.keys():
    ledger.register_hooks()
else:
    ledger.tell('Pandas not imported')

def set_output(tell_method):
    ledger.set_output(tell_method)

def dev_mode():
    from dovpanda.dev import dev_hooks
    dev_hooks(ledger)
