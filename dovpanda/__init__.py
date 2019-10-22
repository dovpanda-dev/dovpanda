import sys

from dovpanda.core import ledger

if 'pandas' in sys.modules.keys():
    ledger.register_hooks()
else:
    ledger.tell('Pandas not imported')


def set_output(tell_method):
    ledger.set_output(tell_method)


def ignore_hook(func_name):
    ledger.ignore_hook(func_name)


def reset_ignores():
    ledger.reset_ignores()
