__author__ = """Dean Langsam"""
__version__ = '0.0.2.alpha'

import sys

from dovpanda.core import ledger

if 'pandas' in sys.modules.keys():
    ledger.register_hints()
else:
    ledger.tell('Pandas not imported')


def set_output(tell_method):
    ledger.set_output(tell_method)
