# test_basic.py
from inventory_application_deep_dive.app.models.basic import addition


def test_basic(demo_fixt) -> None:
    """Basic test to test Continuous Integration works correctly."""
    a, b, expected = demo_fixt
    result = addition(a, b)
    assert result == expected
