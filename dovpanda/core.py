from dovpanda import base
from dovpanda.base import Ledger

ledger = Ledger()


@ledger.add_hook('DataFrame.__init__')
def init_for_checks(*args, **kwargs):
    print('you have construted a df')


@ledger.add_hook('DataFrame.__init__')
def init_another(*args, **kwargs):
    print('another pre hook for init')


@ledger.add_hook('DataFrame.iterrows')
def iterrows_is_bad(*args, **kwargs):
    print("iterrows is not recommended, and in the majority of cases will have better alternatives")


@ledger.add_hook('DataFrame.groupby')
def time_grouping(*args, **kwargs):
    try:
        by = args[1]
    except IndexError:
        by = kwargs.get('by')
    base.listify(by)
    if 'hour' in by:
        print('Seems like you are grouping by time, consider using resample')


@ledger.add_hook('concat', hook_type='post')
def duplicate_index_after_concat(res, *args, **kwargs):
    if res.index.nunique() != len(res.index):
        print('After concatenating you have duplicated indexes values - pay attention')
