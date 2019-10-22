from dovpanda.core import ledger


def dev_hooks(ledger):
    @ledger.add_hook('DataFrame.__init__')
    def init_for_checks(*args, **kwargs):
        ledger.tell('you have construted a df')


    @ledger.add_hook('DataFrame.__init__')
    def init_another(*args, **kwargs):
        ledger.tell('another pre hook for init')

    ledger.register_hooks()
