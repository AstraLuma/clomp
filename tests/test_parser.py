import pytest

from clomp.workspace import tokenize, Stop, ShortArgs, LongArg


@pytest.mark.parametrize('argv,tokes', [
    (['foo', 'bar'], [str, str]),
    (['--foo', 'bar'], [LongArg, str]),
    (['--foo', '--', '-abc'], [LongArg, Stop, ShortArgs]),
])
def test_tokenize_types(argv, tokes):
    parsed = list(tokenize(argv))
    assert all(isinstance(tok, typ) for tok, typ in zip(parsed, tokes))


# Pathological cases:
# -ab-c
# --required -- --foo
# --optional -- --foo
# --required -- foo
# (argparse never considers --, --foo, or -bar valid arguments to flags)

# Marginal cases:
# --required -arg
# --optional -arg
