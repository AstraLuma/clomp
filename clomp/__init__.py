"""
"""
from .actions import *  # noqa


class Clomp:
    root_command = None
    components: dict

    def __init__(self):  # TODO: Big pile of flags
        self.components = {}

    def _make_command(self, func):
        if not hasattr(func, 'children'):
            func.children = []
        if not hasattr(func, 'flags'):
            func.flags = []
        func.command = self._add_subcommand(func)

    def _add_subcommand(self, parent):
        def decorator():  # TODO: Big pile of flags
            def _(func):
                self._make_command(func)
                name = func.__name__
                parent.children[name] = func
                return func
            return _
        return decorator

    def entrypoint(self):  # TODO: Big pile of flags
        def _(func):
            assert self._root_command is None
            self._make_command(func)
            self.root_command = func
            return func
        return _

    def component(self):  # TODO: Big pile of flags
        def _(func):
            name = func.__name__
            self.components[name] = func
            return func
        return _

    def __call__(self):
        """
        Do the thing!
        """
        ...


def flag(*names, dest=..., action=..., doc=None):  # TODO: Big pile of args
    def _(func):
        if not hasattr(func, 'flags'):
            setattr(func, 'flags', [])
        func.flags.append(...)
        return func
    return _


def option(name, dest=..., action=..., doc=None):  # TODO: Big pile of args
    def _(func):
        ...
        return func
    return _
