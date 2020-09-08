"""
"""

OPTIONS_ATTR = '_Clomp__options'
CHILDREN_ATTR = '_Clomp__children'


class Clomp:
    _root_command = None
    components: dict

    def __init__(self):  # TODO: Big pile of flags
        self.components = {}

    def _make_command(self, func):
        if not hasattr(func, CHILDREN_ATTR):
            func.__children = {}
        func.command = self._add_subcommand(func)

    def _add_subcommand(self, parent):
        def decorator():  # TODO: Big pile of flags
            def _(func):
                self._make_command(func)
                name = func.__name__
                parent.__children[name] = func
                return func
            return _
        return decorator

    def entrypoint(self):  # TODO: Big pile of flags
        def _(func):
            assert self._root_command is None
            self._make_command(func)
            self._root_command = func
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


def option(*names, dest=..., action=..., doc=None):  # TODO: Big pile of flags
    def _(func):
        if not hasattr(func, OPTIONS_ATTR):
            setattr(func, OPTIONS_ATTR, [])
        getattr(func, OPTIONS_ATTR).append(...)
        return func
    return _


class StoreConst:
    ...

    def __init__(*_):
        ...
