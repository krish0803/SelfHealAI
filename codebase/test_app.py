import pytest
from codebase.app import divide

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    # This test will fail currently because divide(10, 0) raises ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Current implementation of test_divide_by_zero is correct for the bug,
# but let's make a test that FAILS to simulate a production issue.
def test_production_scenario():
    # If the requirement is to return 0 or handle it gracefully, this test would fail if not handled.
    assert divide(10, 0) == 0
