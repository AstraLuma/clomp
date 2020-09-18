"""
All the algorithms and data structures needed for parsing.
"""
import collections
import collections.abc
import contextlib
import re


# from .accessors import CommandAccessor


class Token:
    pattern = None

    def __init__(self, match=None, **attrs):
        assert bool(match) ^ bool(attrs)
        if match is not None:
            self.text = match.group(0)
            vars(self).update(match.groupdict())
        else:
            vars(self).update(attrs)

    def __str__(self):
        return self.text

    def __repr__(self):
        attrs = ' '.join(f"{name}={value!r}" for name, value in vars(self).items())
        return f"<{type(self).__name__} {attrs}>"

    def __eq__(self, other):
        try:
            return vars(self) == vars(other)
        except TypeError:  # missing __dict__
            return False


class Stop(Token):
    pattern = re.compile('--')


class ShortArgs(Token):
    pattern = re.compile('-(?P<flags>[a-zA-Z]+)')


class LongArg(Token):
    pattern = re.compile('--(?P<flag>[a-zA-Z][-a-zA-Z]*)(?:=(?P<value>.*))?')


def tokenize(argv):
    """
    Scans an argv and turns it into a series of tokens.

    Generates a sequence of Tokens or strings.
    """
    for arg in argv:
        for T in (Stop, ShortArgs, LongArg):
            if m := T.pattern.fullmatch(arg):
                yield T(m)
                break
        else:
            yield arg


def half_baked(tokes):
    """
    Handles Stop
    """
    tokes = iter(tokes)
    for t in tokes:
        if isinstance(t, Stop):
            break
        else:
            yield t

    for t in tokes:
        yield str(t)


class ReversibleIterator:
    """
    An iterator wrapper that allows you to put things back.

    Not thread safe.
    """
    def __init__(self, iterable):
        self._iter = iter(iterable)
        self._returned = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._returned:
            return self._returned.pop(0)
        else:
            return next(self._iter)

    def put_back(self, val):
        self._returned.append(val)


class FlagIndex(collections.abc.Mapping):
    """
    Maintains an index of in-scope flags and where they need to go.
    """
    def __init__(self, command=None):
        self.components = {}
        self.component_flags = {}  # name:str -> (component name, flag object)
        self.command_flags = {}  # name:str -> flag object
        self.component_values = {}  # component name -> {variable name -> value}
        self.command_values = {}  # varialbe name -> value

    def add_component(self, component):
        """
        Add a component to the scope.
        """
        name = ...
        self.components[name] = component
        for flag in ...:
            if flag in self.component_flags:
                raise ...
            self.component_flags[flag.name] = name, flag

    def change_command(self, command):
        """
        Change the current command.
        """
        assert not self.command_values  # FIXME: helpful error
        self.command_flags = {}
        for flag in ...:

            self.command_flags[flag.name] = flag

    def put_value(self, flag, value):
        """
        Save the value for a given flag.
        """
        ...

    @contextlib.contextmanager
    def value_accessors(self, flag):
        yield ..., ...

    def __getitem__(self, flagname):
        ...

    def __iter__(self):
        yield from self.component_flags
        yield from self.command_flags

    def __len__(self):
        return len(self.component_flags) + len(self.command_flags)


ParseResult = collections.namedtuple('ParseResult', [
    'pargs',  # positional arguments
    'kwargs',  # dict mapping argument names to their values
    'components',  # dict mapping component names to their kwargs
])


def parse(clomp, tokes):
    """
    Takes a clomp object and a half-baked sequence of tokens and produces a
    ParseResult.
    """
    current_command = clomp._root_command
    flags = FlagIndex()
    flags.change_command(current_command)
    descending_enabled = True
    command_options = []

    argv = ReversibleIterator(argv)
    for token in tokes:
        if isinstance(arg, (ShortArgs, LongArg)):
            if isinstance(arg, ShortArgs):
                flags = [
                    (f'-{a}', None)
                    for a in arg.flags()
                ]
            else:
                flags = [
                    (f'--{arg.flag()}', arg.value())
                ]
            for flagname, value in flags:
                flagobj = flags[flagname]
                with flags.value_accessors(flagname) as (getter, setter):
                    curvalue = getter()
                    given_value = value
                    newvalue = flagobj.call_action(...)
                    setter(newvalue)
        elif descending_enabled and arg in current_command.children:
            current_command = current_command.children[arg]
            flags.change_command(current_command)
        else:
            descending_enabled = False
            command_options.append(arg)

    return ParseResult(
        command_options,
        ...,
        ...,
    )

    # TODO: Parse command_options into command args
    # TODO: Instantiate fixtures
    # TODO: Merge command flags, command options, and fixtures into kwargs
    # TODO: Call the command
