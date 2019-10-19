import functools
import sys
from collections import defaultdict


class Ledger:
    def __init__(self):
        self.hooks = defaultdict(list)


    def replace(self, original, replacement):
        g = rgetattr(sys.modules['pandas'], original)
        rsetattr(sys.modules['pandas'], original, prefix_function(g, replacement))

    def add_hook(self, original):
        def replaces_decorator(replacement):
            self.hooks[original].append(replacement)

        return replaces_decorator

    def register_hooks(self):
        for k, v in self.hooks.items():
            self.replace(k, v)



def prefix_function(f, pres):
    @functools.wraps(f)
    def run(*args, **kwargs):
        # print(args, kwargs)
        # print (f.__name__)
        for pre in pres:
            pre(*args, **kwargs)
        return f(*args, **kwargs)

    return run


def rgetattr(obj, attr):
    attributes = attr.strip('.').split('.')
    for att in attributes:
        try:
            obj = getattr(obj, att)
        except AttributeError as e:
            raise e
    return obj


def rsetattr(obj, attr, value):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, value)


def only_print(s, *args, **kwargs):
    print(s)
    return lambda x: (args, kwargs)

def listify(val):
    if type(val) is str:
        return [val]
    return val