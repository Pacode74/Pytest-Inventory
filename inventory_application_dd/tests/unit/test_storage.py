"""
Tests for Storage class
Command line: python -m pytest tests/unit/test_storage.py

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

pytestmark = pytest.mark.storage_dd


def test_create(storage, storage_values):
    for attr_name in storage_values:
        assert getattr(storage, attr_name) == storage_values.get(attr_name)


@pytest.mark.parametrize(
    "gb, exception", [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_create_invalid_storage(gb, exception, storage_values):
    storage_values["capacity_gb"] = gb
    with pytest.raises(exception):
        inventory.Storage(**storage_values)


def test_repr(storage):
    assert storage.category in repr(storage)
    assert str(storage.capacity_gb) in repr(storage)
