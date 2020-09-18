import pytest

from clomp.workspace import tokenize, Stop, ShortArgs, LongArg, half_baked


@pytest.mark.parametrize('argv,tokes', [
    (['foo', 'bar'], [str, str]),
    (['--foo', 'bar'], [LongArg, str]),
    (['--foo', '--', '-abc'], [LongArg, Stop, ShortArgs]),
])
def test_tokenize_types(argv, tokes):
    parsed = list(tokenize(argv))
    assert all(isinstance(tok, typ) for tok, typ in zip(parsed, tokes))


@pytest.mark.parametrize('argv,tokes', [
    (['foo', 'bar'], ['foo', 'bar']),
    (['--foo', 'bar'], [LongArg(text='--foo', flag='foo', value=None), 'bar']),
    (
        ['--foo', '--', '-abc'],
        [LongArg(text='--foo', flag='foo', value=None), Stop(text='--'),
         ShortArgs(text='-abc', flags='abc')],
    ),
])
def test_tokenize(argv, tokes):
    parsed = list(tokenize(argv))
    assert parsed == tokes


@pytest.mark.parametrize('argv,tokes', [
    (['foo', 'bar'], ['foo', 'bar']),
    (['--foo', 'bar'], [LongArg(text='--foo', flag='foo', value=None), 'bar']),
    (
        ['--foo', '--', '-abc'],
        [LongArg(text='--foo', flag='foo', value=None), '-abc'],
    ),
])
def test_baking(argv, tokes):
    parsed = list(half_baked(tokenize(argv)))
    assert parsed == tokes


# Pathological cases:
# -ab-c
# --required -- --foo
# --optional -- --foo
# --required -- foo
# (argparse never considers --, --foo, or -bar valid arguments to flags)

# Marginal cases:
# --required -arg
# --optional -arg
