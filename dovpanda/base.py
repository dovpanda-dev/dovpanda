import functools
import sys
from collections import defaultdict


class Ledger:
    def __init__(self):
        self.prefix_hooks = defaultdict(list)
        self.suffix_hooks = defaultdict(list)

    def replace(self, original, replacement, order_type='prefix'):
        g = rgetattr(sys.modules['pandas'], original)
        if order_type == 'prefix':
            rsetattr(sys.modules['pandas'], original, prefix_function(g, replacement))
        else:
            rsetattr(sys.modules['pandas'], original, suffix_function(g, replacement))

    def add_hook(self, original, order_type='prefix'):
        def replaces_decorator(replacement):
            self.prefix_hooks[original].append(replacement) if order_type == 'prefix' else self.suffix_hooks[
                original].append(replacement)

        return replaces_decorator

    def register_hooks(self):
        for k, v in self.prefix_hooks.items():
            self.replace(k, v, 'prefix')
        for k, v in self.suffix_hooks.items():
            self.replace(k, v, 'suffix')


def prefix_function(f, pres):
    @functools.wraps(f)
    def run(*args, **kwargs):
        # print(args, kwargs)
        # print (f.__name__)
        for pre in pres:
            pre(*args, **kwargs)
        return f(*args, **kwargs)

    return run


def suffix_function(f, suffixes):
    @functools.wraps(f)
    def run(*args, **kwargs):
        res = f(*args, **kwargs)
        for suffix in suffixes:
            suffix(res, *args, **kwargs)
        return res

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
