"""
Tests for CPU class
Command line: python -m pytest tests/unit/test_cpu.py

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

pytestmark = pytest.mark.cpu_dd


def test_create_cpu(cpu, cpu_values):
    for attr_name in cpu_values:
        assert getattr(cpu, attr_name) == cpu_values.get(attr_name)


@pytest.mark.parametrize(
    "cores, exception", [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_create_invalid_cores(cores, exception, cpu_values):
    cpu_values["cores"] = cores
    with pytest.raises(exception):
        inventory.CPU(**cpu_values)


@pytest.mark.parametrize(
    "watts, exception", [(10.5, TypeError), (-1, ValueError), (0, ValueError)]
)
def test_create_invalid_power(watts, exception, cpu_values):
    cpu_values["power_watts"] = watts
    with pytest.raises(exception):
        inventory.CPU(**cpu_values)


def test_repr(cpu):
    assert cpu.category in repr(cpu)
    assert cpu.name in repr(cpu)
    assert cpu.socket in repr(cpu)
    assert str(cpu.cores) in repr(cpu)
