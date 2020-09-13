"""
All the algorithms and data structures needed for parsing.
"""
import collections.abc


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

    # def put_value(self, flag, value):
    #     """
    #     Save the value for a given flag.
    #     """
    #     ...

    def __getitem__(self, flagname):
        ...

    def __iter__(self):
        ...

    def __len__(self):
        ...


def iter_flags(arg):
    """
    Breaks up a flag.

    If a double-dash, returns just the arg.

    If a single, produces each letter.

    Dashes are included.
    """
    assert arg.startswith('-')
    if arg.startswith('--'):
        yield arg
    else:
        for letter in arg[1:]:
            yield f'-{letter}'


def _resolve(clomp, argv):
    """
    Run the resolution algorithm
    """
    current_command = clomp._root_command
    found_fixtures = get_fixtures(current_command)
    flags = FlagIndex()
    flags.change_command(current_command)
    dash_parsing = True
    descending_enabled = True
    command_options = []

    argv = ReversibleIterator(argv)
    for arg in argv:
        if arg == '--':
            dash_parsing = False
        elif dash_parsing and arg.startswith('-'):
            for flagname in iter_flags(arg):
                flagobj = flags[flagname]
                value = flagobj.call_action(argv)
                flags.set_value(value)
        elif descending_enabled and arg in current_command.__children:
            current_command = current_command.__children[arg]
            flags.change_command(current_command)
        else:
            descending_enabled = False
            command_options.append(arg)

    # TODO: Parse command_options into command args
    # TODO: Instantiate fixtures
    # TODO: Merge command flags, command options, and fixtures into kwargs
    # TODO: Call the command

 