clomp - CLI by Composition
==========================

Example
-------

```python
cli = Clomp()

@cli.component()
@clomp.option('--verbose', dest='log_level', action='store_const', const='warning')
@clomp.option('--quiet', dest='log_level', action='store_const', const='debug')
def verbosity(log_level='info'):
    ...

@cli.entrypoint()
def main(verbosity):
    pass


@cli.component()
@clomp.option('--name')
def widget(name=...):
    if name is ...:
        return widget_from_pwd()
    else:
        return widget_from_name(name)

@main.command()
def info(widget)
    pretty_print(widget)
```
