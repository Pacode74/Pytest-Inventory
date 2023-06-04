"""
Tests for HDD class
Command line: python -m pytest tests/unit/test_hdd.py

To run a specific test:
Command line: python -m pytest inventory_application_dd/tests/unit/test_validators.py::TestIntegerValidator::test_error

To run test under specific pattern:
Command line: pytest -k "test_validate or test_some_other_test"

I want to apply the same marker for all below pytest:
pytestmark = pytest.mark.storage_dd
Also need to register the marker in pytest.ini
Command line: pytest -m validate

To check coverage: $ coverage run -m pytest .
To generate coverage report: $ coverage html
"""

import pytest

from inventory_application_dd.apps.models import inventory

pytestmark = pytest.mark.hdd_dd


def test_create(hdd, hdd_values):
    for attr_name in hdd_values:
        assert getattr(hdd, attr_name) == hdd_values.get(attr_name)


@pytest.mark.parametrize("size", ["2.5", '5.25"'])
def test_create_invalid_size(size, hdd_values):
    hdd_values["size"] = size
    with pytest.raises(ValueError):
        inventory.HDD(**hdd_values)


@pytest.mark.parametrize(
    "rpm, exception", [("100", TypeError), (100, ValueError), (100_000, ValueError)]
)
def test_create_invalid_rpm(rpm, exception, hdd_values):
    hdd_values["rpm"] = rpm
    with pytest.raises(exception):
        inventory.HDD(**hdd_values)


def test_repr(hdd):
    assert hdd.category in repr(hdd)
    assert str(hdd.capacity_gb) in repr(hdd)
    assert hdd.size in repr(hdd)
    assert str(hdd.rpm) in repr(hdd)
