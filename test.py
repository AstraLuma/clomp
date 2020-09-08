from dataclasses import dataclass
import logging
import pathlib
from pprint import pprint

from clomp import Clomp, option, StoreConst


@dataclass
class Widget:
    name: str


cli = Clomp()


@cli.component()
@option('--verbose', dest='log_level', action=StoreConst('debug'))
@option('--quiet', dest='log_level', action=StoreConst('warning'))
def verbosity(log_level='info'):
    logging.basicConfig(level=log_level)


@cli.entrypoint()
def main(verbosity):
    """
    Manipulate widgets
    """


@cli.component()
@option('--name', doc="Name of widget (default: infer from current directory)")
def widget(name=...):
    if name is ...:
        return Widget(name=pathlib.Path.cwd().name)
    else:
        return Widget(name=name)


@main.command()
def info(widget):
    """
    Print info about a widget
    """
    pprint(widget)


if __name__ == '__main__':
    cli()
