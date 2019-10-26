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
except (ModuleNotFoundError, ImportError):
    pass


class Hint:
    def __init__(self, original, hook_type, replacement):
        accepted_hooks = ['pre', 'post']
        assert hook_type in accepted_hooks, f'hook_type must be one of {accepted_hooks}'

        self.original = original
        self.hook_type = hook_type
        self.replacement = replacement


class _Teller:
    def __init__(self):
        self.message = None
        self.set_output('display')
        self.line = None
        self.lineno = None
        self.verbose = True

    def __repr__(self):
        trace = self.if_verbose(f' (Line {self.lineno})')
        return self._strip_html(f'===== {self.message} ====={trace}')

    def __str__(self):
        trace = self.if_verbose(f' (Line {self.lineno})')
        return f'{self._strip_html(self.message)}{trace}'

    def __call__(self, s):
        self.tell(s)

    def _repr_html_(self):
        return self.nice_output()

    def nice_output(self):
        trace = f'<div style="font-size:0.7em;">Line {self.lineno}: <code>{self.line}</code> </div>'
        trace = self.if_verbose(trace)
        html = f'''
        <div class="alert alert-info" role="alert">
          {self.message}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          {trace}

        </div>
        '''
        return html

    @staticmethod
    def _strip_html(s):
        return re.sub('<[^<]+?>', '', s)

    @staticmethod
    def _no_output(*args, **kwargs):
        return

    def if_verbose(self, s):
        if self.verbose:
            return s
        else:
            return ''

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
            except (ModuleNotFoundError, ImportError):
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
        self.hints = defaultdict(list)
        self.teller = _Teller()
        self.verbose = True
        self.caller_filename = None

    def replace(self, original, func_hooks: tuple):
        g = rgetattr(sys.modules['pandas'], original)
        rsetattr(sys.modules['pandas'], original, self.attach_hooks(g, func_hooks))

    def add_hint(self, original, hook_type='pre'):

        def replaces_decorator(replacement):
            hint = Hint(original=original, hook_type=hook_type, replacement=replacement)
            self.hints[original].append(hint)

        return replaces_decorator

    def register_hints(self):
        for original, func_hooks in self.hints.items():
            self.replace(original, func_hooks)

    def attach_hooks(self, f, func_hooks):
        pres = [hook.replacement for hook in func_hooks if hook.hook_type == 'pre']
        posts = [hook.replacement for hook in func_hooks if hook.hook_type == 'post']

        @functools.wraps(f)
        def run(*args, **kwargs):
            caller = traceback.extract_stack()[-2]
            self._set_caller_details(caller)
            if self.inner_pandas:
                ret = f(*args, **kwargs)
            else:
                for pre in pres:
                    pre(*args, **kwargs)
                ret = f(*args, **kwargs)
                for post in posts:
                    post(ret, *args, **kwargs)
            return ret

        return run

    def _set_caller_details(self, caller):
        self.caller_filename = caller.filename
        self.inner_pandas = self.caller_filename.startswith(PANDAS_DIR)
        if self.caller_filename.startswith(PANDAS_DIR):
            return
        self.teller.line = caller.line
        self.teller.lineno = caller.lineno

    # Output
    def tell(self, *args, **kwargs):
        self.teller(*args, *kwargs)

    def set_output(self, output):
        self.teller.set_output(output)

    def set_verbose(self, verbose=True):
        self.teller.verbose = verbose


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
