import functools
import pathlib
import re
import sys
import traceback
from collections import defaultdict

import pandas

PANDAS_DIR = str(pathlib.Path(pandas.__file__).parent.absolute())
try:  # If user runs from notebook they will have this
    from IPython.display import display
except:
    pass


class Teller:
    def __init__(self):
        self.message = None
        self.set_output('display')

    def __repr__(self):
        return self._strip_html(f'===== {self.message} =====')

    def __str__(self):
        return self._strip_html(self.message)

    def _repr_html_(self):
        return nice_output(self.message)

    def __call__(self, s):
        self.tell(s)

    @staticmethod
    def _strip_html(s):
        return re.sub('<[^<]+?>', '', s)
    @staticmethod
    def _no_output(*args, **kwargs):
        return

    def set_output(self, output_method):
        accepted_methods = ['print', 'display', 'debug', 'info', 'warning', 'off']
        if type(output_method) is str:
            assert output_method in accepted_methods, f'output_format must be one of {accepted_methods} or a callable'
        if output_method == 'print':
            self.output = print
        elif output_method in ['debug', 'info', 'warning']:
            try:
                from loguru import logger
            except ModuleNotFoundError:
                import logging
                logger = logging.getLogger('dovpanda')
            self.output = getattr(logger, output_method)
        elif output_method == 'display':
            try:
                self.output = display
            except:
                self.set_output('print')
        elif output_method == 'off':
            self.output = self._no_output
        else:
            self.output = output_method

    def tell(self, message):
        self.message = message
        self.output(self)


class Ledger:
    def __init__(self):
        self.hooks = defaultdict(list)
        self.teller = Teller()

    def replace(self, original, func_hooks: tuple):
        g = rgetattr(sys.modules['pandas'], original)
        rsetattr(sys.modules['pandas'], original, self.attach_hooks(g, func_hooks))

    def add_hook(self, original, hook_type='pre'):
        accepted_hooks = ['pre', 'post']
        assert hook_type in accepted_hooks, f'hook_type must be one of {accepted_hooks}'

        def replaces_decorator(replacement):
            self.hooks[original].append((replacement, hook_type))

        return replaces_decorator

    def register_hooks(self):
        for original, func_hooks in self.hooks.items():
            self.replace(original, func_hooks)

    def tell(self, *args, **kwargs):
        self.teller(*args, *kwargs)

    def set_output(self, output):
        self.teller.set_output(output)

    def attach_hooks(self, f, func_hooks):
        pres = [hook_function for (hook_function, hook_type) in func_hooks if hook_type.lower().startswith('pre')]
        posts = [hook_function for (hook_function, hook_type) in func_hooks if hook_type.lower().startswith('post')]

        @functools.wraps(f)
        def run(*args, **kwargs):
            caller = traceback.extract_stack()[-2].filename
            if caller.startswith(PANDAS_DIR):
                ret = f(*args, **kwargs)
            else:
                for pre in pres:
                    pre(*args, **kwargs)
                ret = f(*args, **kwargs)
                for post in posts:
                    post(ret, *args, **kwargs)
            return ret

        return run


def nice_output(s):
    html = f'''
    <div class="alert alert-info" role="alert">
      {s}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
    '''
    return html


def get_arg(args, kwargs, which_arg, which_kwarg):
    try:
        ret = args[which_arg]
    except IndexError:
        ret = kwargs.get(which_kwarg)
    return ret


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

def setify(val):
    return set(listify(val))
