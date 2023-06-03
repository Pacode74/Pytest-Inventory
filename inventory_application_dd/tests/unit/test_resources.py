"""
Tests for Resource class
Command line: python -m pytest tests/unit/test_resource.py

To run a specific test:
Command line: python -m pytest inventory_application_dd/tests/unit/test_validators.py::TestIntegerValidator::test_error

To run test under specific pattern:
Command line: pytest -k "test_validate or test_some_other_test"

I want to apply the same marker for all below pytest:
pytestmark = pytest.mark.resources_dd
Also need to register the marker in pytest.ini
Command line: pytest -m validate

To check coverage: $ coverage run -m pytest .
To generate coverage report: $ coverage html
"""

import pytest

from inventory_application_dd.apps.models import inventory

pytestmark = pytest.mark.resources_dd


# --------- easy test-----------------------
def test_create_resource():
    resource = inventory.Resource("Parrot", "Pirates A-Hoy", 100, 50)
    assert resource.name == "Parrot"
    assert resource.manufacturer == "Pirates A-Hoy"
    assert resource.total == 100
    assert resource.allocated == 50


def test_create_resource_use_fixture(resource_values, resource):
    assert resource.name == resource_values["name"]
    assert resource.manufacturer == resource_values["manufacturer"]
    assert resource.total == resource_values["total"]
    assert resource.allocated == resource_values["allocated"]


# -------------------get attribute test -------------------
def test_create_resource_getattr(resource_values, resource):
    for attr_name in resource_values:
        assert getattr(resource, attr_name) == resource_values.get(attr_name)


# ---------------- test raise exceptions-------------------------
def test_create_invalid_total_type():
    with pytest.raises(TypeError):
        inventory.Resource("Parrot", "Pirates A-Hoy", 10.5, 5)


def test_create_invalid_allocated_type():
    with pytest.raises(TypeError):
        inventory.Resource("name", "manu", 10, 2.5)


def test_create_invalid_total_value():
    with pytest.raises(ValueError):
        inventory.Resource("name", "manu", -10, 0)


@pytest.mark.parametrize("total,allocated", [(10, -5), (10, 20)])
def test_create_invalid_allocated_value(total, allocated):
    with pytest.raises(ValueError):
        inventory.Resource("name", "manu", total, allocated)


@pytest.mark.parametrize("value", [-1, 0, 1_000])
def test_claim_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.claim(value)


@pytest.mark.parametrize("value", [-1, 0, 1_000])
def test_freeup_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.freeup(value)


# ---------- testing property attributes-------------


def test_total(resource):
    assert resource.total == resource._total


def test_allocated(resource):
    assert resource.allocated == resource._allocated


def test_available(resource, resource_values):
    assert resource.available == resource.total - resource.allocated


def test_category(resource):
    assert resource.category == "resource"


def test_str_repr(resource):
    assert str(resource) == resource.name


def test_repr_repr(resource):
    assert repr(resource) == "{} ({} - {}) : total={}, allocated={}".format(
        resource.name,
        resource.category,
        resource.manufacturer,
        resource.total,
        resource.allocated,
    )


def test_claim(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.claim(n)
    assert resource.total == original_total  # the total has not changed.
    assert resource.allocated == original_allocated + n  # the allocated has changed.


def test_freeup(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.freeup(n)
    assert resource.allocated == original_allocated - n
    assert resource.total == original_total


def test_died(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.died(n)
    assert resource.total == original_total - n
    assert resource.allocated == original_allocated - n


@pytest.mark.parametrize("value", [-1, 0, 1_000])
def test_died_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.died(value)


def test_purchased(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.purchased(n)
    assert resource.total == original_total + n
    assert resource.allocated == original_allocated


@pytest.mark.parametrize("value", [-1, 0])
def test_purchased_invalid(resource, value):
    with pytest.raises(ValueError):
        resource.purchased(value)
