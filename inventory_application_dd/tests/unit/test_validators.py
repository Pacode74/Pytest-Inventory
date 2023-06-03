"""
Tests the validator functions
To run the test in the file:
Command line: python -m pytest tests/unit/test_validators.py

To run a specific test:
Command line: python -m pytest inventory_application_dd/tests/unit/test_validators.py::TestIntegerValidator::test_error

To run test under specific pattern:
Command line: pytest -k "test_validate or test_some_other_test"

I want to apply the same marker for all below pytest:
pytestmark = pytest.mark.validate
Also need to register the marker in pytest.ini
Command line: pytest -m validate

To check coverage: $ coverage run -m pytest .
To generate coverage report: $ coverage html
"""

import pytest

from inventory_application_dd.apps.utils.validators import validate_integer

pytestmark = pytest.mark.validate


class TestIntegerValidator:
    def test_validate(self):
        validate_integer(
            arg_name="arg",
            arg_value=10,
            min_value=0,
            max_value=20,
            custom_min_message="custom min msg",
            custom_max_message="custom max message",
        )

    def test_error(self):
        with pytest.raises(TypeError):
            validate_integer(arg_name="arg", arg_value=1.5)

    def test_min_str_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer(arg_name="arg", arg_value=10, min_value=100)
        # print(f'{ex.value=}') => 'arg cannot be less than 100'
        assert "arg" in str(ex.value)
        assert "100" in str(ex.value)

    def test_min_custom_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer(
                arg_name="arg", arg_value=10, min_value=100, custom_min_message="custom"
            )
        assert str(ex.value) == "custom"

    def test_max_std_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer(arg_name="arg", arg_value=10, min_value=1, max_value=5)
        assert "arg" in str(ex.value)
        assert "5" in str(ex.value)

    def test_max_custom_err_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer(
                arg_name="arg",
                arg_value=10,
                min_value=1,
                max_value=5,
                custom_max_message="custom",
            )
        assert str(ex.value) == "custom"
