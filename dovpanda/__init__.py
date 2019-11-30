__author__ = """Dean Langsam"""
__version__ = '0.0.5'

import sys

from dovpanda import tips
from dovpanda.core import ledger


def set_output(tell_method):
    ledger.set_output(tell_method)


def start():
    """Startup `dovpanda`, in case it has been shut down. This is called when importing `dovpanda`"""
    ledger.register_hints()


def shutdown():
    """Shutdown `dovpanda`. Register original pandas methods back to their namespace"""
    ledger.revert()


mute = ledger.mute


def tip():
    return tips.random_tip()


if 'pandas' in sys.modules.keys():
    start()
else:
    ledger.tell('Pandas not imported')
