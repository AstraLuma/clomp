clomp - CLI by Composition
==========================

Example
-------

```python
import logging

from clomp import Clomp, option, StoreConst

from . import widget_from_pwd, widget_from_name, pretty_print


cli = Clomp()


@cli.component()
@option('--verbose', dest='log_level', action=StoreConst('debug'))
@option('--quiet', dest='log_level', action=StoreConst('warning'))
def verbosity(log_level='info'):
    logging.getLogger().setLevel(log_level)


@cli.entrypoint()
def main(verbosity):
    """
    Manipulate widgets and other things
    """


@cli.component()
@option('--name', doc="Name of widget (default: infer from current directory)")
def widget(name=...):
    if name is ...:
        return widget_from_pwd()
    else:
        return widget_from_name(name)


@main.command()
def info(widget):
    """
    Print info about a widget
    """
    pretty_print(widget)


if __name__ == '__main__':
    cli()
```
