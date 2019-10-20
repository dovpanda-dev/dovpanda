import functools
import sys
from collections import defaultdict


class Ledger:
    def __init__(self):
        self.hooks = defaultdict(list)

    def replace(self, original, hooks: tuple):
        g = rgetattr(sys.modules['pandas'], original)
        rsetattr(sys.modules['pandas'], original, attach_hooks(g, hooks))

    def add_hook(self, original, hook_type='pre'):
        accepted_hooks = ['pre', 'post']
        assert hook_type in accepted_hooks, f'hook_type must be one of {accepted_hooks}'

        def replaces_decorator(replacement):
            self.hooks[original].append((replacement, hook_type))

        return replaces_decorator

    def register_hooks(self):
        for original, func_hooks in self.hooks.items():
            self.replace(original, func_hooks)


def attach_hooks(f, hooks):
    pres = [hook_function for (hook_function, hook_type) in hooks if hook_type.lower().startswith('pre')]
    posts = [hook_function for (hook_function, hook_type) in hooks if hook_type.lower().startswith('post')]

    @functools.wraps(f)
    def run(*args, **kwargs):
        for pre in pres:
            pre(*args, **kwargs)
        ret = f(*args, **kwargs)
        for post in posts:
            post(ret, *args, **kwargs)
        return ret

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
