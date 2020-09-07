"""
"""

OPTIONS_ATTR = '_Clomp__options'
CHILDREN_ATTR = '_Clomp__children'


class Clomp:
    entrypoint = None
    components: dict

    def __init__(self):
        self.components = {}

    def _make_command(self, func):
        if not hasattr(func, CHILDREN_ATTR):
            func.__children = {}
        func.command = self._add_subcommand(func)

    def _add_subcommand(self, parent):
        def decorator():
            def _(func):
                self._make_command(func)
                name = func.__name__
                parent.__children[name] = func
                return func
            return _
        return decorator

    def entrypoint(self):
        def _(func):
            self._make_command(func)
            self.entrypoint = func
            return func
        return _

    def component(self):
        def _(func):
            name = func.__name__
            self.components[name] = func
            return func
        return _


def option(name):  # TODO: Big pile of flags
    def _(func):
        if not hasattr(func, OPTIONS_ATTR):
            setattr(func, OPTIONS_ATTR, [])
        getattr(func, OPTIONS_ATTR).append(...)
        return func
