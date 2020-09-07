clomp - CLI by Composition
==========================

Example
-------

```python
import logging

from clomp import Clomp, option

from . import widget_from_pwd, widget_from_name, pretty_print


cli = Clomp()


@cli.component()
@option('--verbose', dest='log_level', action='store_const', const='warning')
@option('--quiet', dest='log_level', action='store_const', const='debug')
def verbosity(log_level='info'):
    logging.getLogger().setLevel(log_level)


@cli.entrypoint()
def main(verbosity):
    pass


@cli.component()
@option('--name')
def widget(name=...):
    if name is ...:
        return widget_from_pwd()
    else:
        return widget_from_name(name)


@main.command()
def info(widget):
    pretty_print(widget)


if __name__ == '__main__':
    cli()
```
