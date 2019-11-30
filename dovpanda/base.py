import ast
import functools
import inspect
import re
import sys
from collections import defaultdict, deque
from contextlib import contextmanager
from itertools import chain
from dovpanda import config

try:  # If user runs from notebook they will have this
    from IPython.display import display
except (ModuleNotFoundError, ImportError):
    pass


class Hint:
    def __init__(self, original, hook_type, replacement, *, stop_nudge=1):
        accepted_hooks = ['pre', 'post']
        assert hook_type in accepted_hooks, f'hook_type must be one of {accepted_hooks}'

        self.original = original
        self.hook_type = hook_type
        self.replacement = replacement
        self.stop_nudge = stop_nudge

    def __repr__(self):
        return (f"[HINT] Hooks on {self.original} with {self.replacement} "
                f"at {self.hook_type} but stops after {self.stop_nudge}")

    def __str__(self):
        return (f'{self.replacement.__name__} hooks on {self.original}')


class _Teller:
    def __init__(self):
        self.message = None
        self.set_output('display')
        self.verbose = True
        self.caller = None

    def __repr__(self):
        trace = self.if_verbose(f'(Line {self.caller.lineno}) ')
        return self._strip_html(f'* ====={trace} {self.message} =====\n')

    def __str__(self):
        trace = self.if_verbose(f'(Line {self.caller.lineno}) ')
        return f'* {trace}{self._strip_html(self.message)}\n'

    def _repr_html_(self):
        return self.nice_output()

    def nice_output(self):
        code_context = self.caller.code_context[0].strip()
        html = config.html_tell.format(
            level=self.level,
            logo_tag=config.logo_tag,
            message=self.message,
            lineno=self.caller.lineno,
            code_context=code_context
        )
        return html

    @staticmethod
    def _strip_html(s):
        s = re.sub(r'\n', '', s)
        s = re.sub(r'<br>', r'\n', s)
        s = re.sub(r' {2,}', r' ', s)
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
            except NameError:
                self.set_output('print')
        elif output_method == 'off':
            self.output = self._no_output
        else:
            self.output = output_method

    def tell(self, message, color='blue'):
        self.level = config.color_to_level.get(color, 'blue')
        self.message = message
        self.output(self)


class Ledger:
    def __init__(self):
        self.hints = defaultdict(list)
        self.teller = _Teller()
        self.verbose = True
        self.caller = None
        # TODO: Memory has a cache only of registered methods. Change to accomodate all pandas
        self.memory = deque(maxlen=32)
        self.original_methods = dict()

    def __len__(self):
        hints_gen = chain.from_iterable(self.hints.values())
        return len(list(hints_gen))

    def nunique(self):
        hints_gen = chain.from_iterable(self.hints.values())
        return len(set(hints_gen))

    def replace(self, original, func_hooks):
        g = rgetattr(sys.modules['pandas'], original)
        self.save_original(original, g)
        rsetattr(sys.modules['pandas'], original, self.attach_hooks(g, func_hooks))

    def add_hint(self, originals, hook_type='pre', stop_nudge=1):

        def replaces_decorator(replacement):
            hint = Hint(original=originals, hook_type=hook_type, replacement=replacement,
                        stop_nudge=stop_nudge)
            for original in listify(originals):
                self.hints[original].append(hint)

        return replaces_decorator

    def register_hints(self):
        for original, func_hooks in self.hints.items():
            self.replace(original, func_hooks)

    def attach_hooks(self, f, func_hooks):
        pres = [hook for hook in func_hooks if hook.hook_type == 'pre']
        posts = [hook for hook in func_hooks if hook.hook_type == 'post']

        @functools.wraps(f)
        def run(*args, **kwargs):
            self._set_caller_details(f)
            arguments = self._get_arguments(f, *args, **kwargs)
            self.run_hints(pres, arguments)
            ret = f(*args, **kwargs)
            self.run_hints(posts, ret, arguments)
            return ret

        return run

    def run_hints(self, hints, *args):
        if self.resticted_dirs():
            return
        for hint in hints:
            try:
                if self.similar <= hint.stop_nudge:
                    hint.replacement(*args)
            except Exception as e:
                self.tell(config.html_bug.format(hint=hint, e=e), color='red')

    def _get_arguments(self, f, *args, **kwargs):
        sig = inspect.signature(f).bind(*args, **kwargs)
        sig.apply_defaults()
        sig.arguments['_dovpanda'] = {'source_func_name': f.__name__}
        return sig.arguments

    def _set_caller_details(self, f):
        frame = inspect.currentframe().f_back.f_back
        self.caller = inspect.getframeinfo(frame)
        if self.resticted_dirs():
            return
        self._update_memory(f)
        self.teller.caller = self.caller

    def _update_memory(self, f):
        self.memory.append((f, self.caller))
        latest = self.memory[-1]
        similar = [caller for caller in self.memory if caller == latest]
        similar = len(similar)
        self.similar = similar

    def resticted_dirs(self):
        caller_file = self.caller.filename
        if any([caller_file.startswith(str(dir_name)) for dir_name in config.RESTRICTED_DIRS]):
            return True
        return False

    # Output

    def tell(self, *args, **kwargs):
        self.teller.tell(*args, **kwargs)

    def set_output(self, output):
        self.teller.set_output(output)

    def set_verbose(self, verbose=True):
        self.teller.verbose = verbose

    def save_original(self, original_name, original_function):
        if original_name in self.original_methods:
            return
        else:
            self.original_methods[original_name] = original_function

    def revert(self):
        """Revert the ledger. Register original pandas methods back to their namespace"""
        for original_name, original_func in self.original_methods.items():
            rsetattr(sys.modules['pandas'], original_name, original_func)

    @contextmanager
    def mute(self):
        current_output = self.teller.output
        self.set_output('off')
        try:
            yield
        except Exception as e:
            raise e
        finally:
            self.set_output(current_output)


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
    if type(val) in [str, int, float]:
        return [val]
    return val


def setify(val):
    return set(listify(val))


def is_assignment(caller):
    try:
        node = ast.parse(caller.code_context[0])
    except SyntaxError:
        return False

    return isinstance(node.body[0], ast.Assign)


def get_assignee(caller):
    if not is_assignment(caller):
        return
    node = ast.parse(caller.code_context[0])
    assignee = node.body[0].targets[0].id
    return assignee
