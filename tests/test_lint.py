import inspect
import pytest
from pylint.lint import Run
from pylint.reporters import CollectingReporter


import onono


@pytest.fixture(params=[
    onono.app,
    onono.gamelogic,
    onono.menu,
    onono.image,
    onono.savegame
])
def linter(request):
    """Test codestyle for various src files."""
    print(f"Module: {request.param.__name__}")

    src_file = inspect.getfile(request.param)
    rep = CollectingReporter()
    # disabled warnings:
    # C0301 line too long
    # C0103 variables name (does not like shorter than 2 chars)
    # E1101 Module 'pygame' has no '...' member (no-member)
    #       This is caused by bad interaction between pygame and pylint.
    # E0401 (import-error): Unable to import '...'
    #       Two different import systems (from __init__ and __main__)
    r = Run(
        ["--disable=C0301,C0103,E1101,E0401", "-sn", src_file],
        reporter=rep,
        exit=False,
    )
    return r.linter


def test_codestyle_score(linter):
    """Evaluate codestyle for different thresholds."""
    print("\nLinter output:")
    for m in linter.reporter.messages:
        print(f"{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}")
    score = linter.stats.global_note

    print(f"pylint score = {score}")
    for limit in range(11):
        assert score >= limit
