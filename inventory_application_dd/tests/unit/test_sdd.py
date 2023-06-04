"""
Tests for SSD class
Command line: python -m pytest tests/unit/test_ssd.py

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

pytestmark = pytest.mark.sdd_dd


def test_create(ssd, ssd_values):
    for attr_name in ssd_values:
        assert getattr(ssd, attr_name) == ssd_values.get(attr_name)


def test_repr(ssd):
    assert ssd.category in repr(ssd)
    assert str(ssd.capacity_gb) in repr(ssd)
    assert ssd.interface in repr(ssd)
