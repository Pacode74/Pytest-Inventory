import pytest
from inventory_application.apps.cpu import CPU
from pytest_check import check
import inspect
import types

"""
Tests for CPU class
Command line: python -m pytest tests/unit/test_cpu.py

To run a specific test:
Command line: python -m pytest inventory_application_dd/tests/unit/test_validators.py::TestIntegerValidator::test_error

To run test under specific pattern:
Command line: pytest -k "test_validate or test_some_other_test"

I want to apply the same marker for all below pytest:
pytestmark = pytest.mark.xyz or pytestmark = [pytest.mark.xyz, pytest.mark.abc]
Also need to register the marker in pytest.ini
Command line: pytest -m validate

To check coverage: $ coverage run -m pytest .
To generate coverage report: $ coverage html
"""

pytestmark = pytest.mark.cpu

# ----------------------- Easy level tests: test CPU with different values ----


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("Intel-core", "Intel", "Intel-core", "Intel"),
        ("AMD-i9", "AMD", "AMD-i9", "AMD"),
        ("Intel-Pentium", "Intel", "Intel-Pentium", "Intel"),
    ],
)
def test_name_manufacturer_cpu(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    with check:
        assert r.name == expected_name
    with check:
        assert r.manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("Intel-core", "Intel", "Intel-core", "Intel"),
        ("AMD-i9", "AMD", "AMD-i9", "AMD"),
        ("Intel-Pentium", "Intel", "Intel-Pentium", "Intel"),
    ],
)
def test_private_name_manufacture_cpu(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    with check:
        assert r._name == expected_name
    with check:
        assert r._manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, new_name, new_manufacturer, expected_name, expected_manufacturer",
    [
        (
            "Intel-core",
            "Intel",
            "New-Intel-core",
            "New-Intel",
            "New-Intel-core",
            "New-Intel",
        ),
        ("AMD-i9", "AMD", "New-AMD-i9", "New-AMD", "New-AMD-i9", "New-AMD"),
        (
            "Intel-Pentium",
            "Intel",
            "New-Intel-Pentium",
            "New-Intel",
            "New-Intel-Pentium",
            "New-Intel",
        ),
    ],
)
def test_setter_for_name_manufacturer_cpu(
    name: str,
    manufacturer: str,
    new_name: str,
    new_manufacturer: str,
    expected_name: str,
    expected_manufacturer: str,
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    with check:
        r.name = new_name
        assert r.name == expected_name
    with check:
        r.manufacturer = new_manufacturer
        assert r.manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, cores, socket, power_watts, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            7,
            "AM5",
            93,
            dict(
                category="cpu",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=6,
                allocated=1,
                remaining=5,
                cores=7,
                socket="AM5",
                power_watts=93,
            ),
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            5,
            "AM3",
            95,
            dict(
                category="cpu",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=9,
                allocated=0,
                remaining=9,
                cores=5,
                socket="AM3",
                power_watts=95,
            ),
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            9,
            "AM4",
            94,
            dict(
                category="cpu",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=9,
                allocated=1,
                remaining=8,
                cores=9,
                socket="AM4",
                power_watts=94,
            ),
        ),
    ],
)
def test_total_allocated_remaining_category_property_cpu(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    cores: int,
    socket: str,
    power_watts: int,
    expected: dict,
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.cores = cores
    r.socket = socket
    r.power_watts = power_watts
    with check:
        assert r.total == expected["total"]
    with check:
        assert r.allocated == expected["allocated"]
    with check:
        assert r.remaining == expected["remaining"]
    with check:
        assert r.category == expected["category"]
    with check:
        assert r.cores == expected["cores"]
    with check:
        assert r.socket == expected["socket"]
    with check:
        assert r.power_watts == expected["power_watts"]


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, cores, socket, power_watts, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            5,
            "AM3",
            92,
            "CPU(category='cpu', name='Intel-core', manufacturer='Intel', total=6, allocated=1, remaining=5, core=5, "
            "socket='AM3', power_watts=92)",
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            7,
            "AM5",
            93,
            "CPU(category='cpu', name='AMD-i9', manufacturer='AMD', total=9, allocated=0, remaining=9, core=7, "
            "socket='AM5', power_watts=93)",
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            9,
            "AM4",
            94,
            "CPU(category='cpu', name='Intel-Pentium', manufacturer='Intel', total=9, allocated=1, remaining=8, "
            "core=9, socket='AM4', power_watts=94)",
        ),
    ],
)
def test_repr_method_v1_cpu(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    cores: int,
    socket: str,
    power_watts: int,
    expected: str,
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.cores = cores
    r.socket = socket
    r.power_watts = power_watts
    assert repr(r) == expected


def test_repr_method_v2_cpu(repr_fixt_cpu) -> None:
    (
        name,
        manufacturer,
        purchase,
        claim,
        freeup,
        died,
        cores,
        socket,
        power_watts,
        expected,
    ) = repr_fixt_cpu
    r = CPU(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.cores = cores
    r.socket = socket
    r.power_watts = power_watts
    assert repr(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, expected",
    [
        (
            "Intel-core",
            "Intel",
            "CPU(name='Intel-core', manufacturer='Intel')",
        ),
        (
            "AMD-i9",
            "AMD",
            "CPU(name='AMD-i9', manufacturer='AMD')",
        ),
        (
            "Intel-Pentium",
            "Intel",
            "CPU(name='Intel-Pentium', manufacturer='Intel')",
        ),
    ],
)
def test_str_method_v1_cpu(
    name: str,
    manufacturer: str,
    expected: str,
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    assert str(r) == expected


def test_str_method_v2_cpu(str_fixt_cpu) -> None:
    name, manufacturer, expected = str_fixt_cpu
    r = CPU(name=name, manufacturer=manufacturer)
    assert str(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, cores, socket, power_watts, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            5,
            "AM3",
            92,
            "CPU(category='cpu', name='Intel-core', manufacturer='Intel', total=6, allocated=1, remaining=5, core=5, "
            "socket='AM3', power_watts=92)",
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            7,
            "AM5",
            93,
            "CPU(category='cpu', name='AMD-i9', manufacturer='AMD', total=9, allocated=0, remaining=9, core=7, "
            "socket='AM5', power_watts=93)",
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            9,
            "AM4",
            94,
            "CPU(category='cpu', name='Intel-Pentium', manufacturer='Intel', total=9, allocated=1, remaining=8, "
            "core=9, socket='AM4', power_watts=94)",
        ),
    ],
)
def test_convert_str_to_instance_cpu(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    expected: str,
    cores: int,
    socket: str,
    power_watts: int,
) -> None:
    r = CPU(name=name, manufacturer=manufacturer)
    rr = eval(str(r))
    rr.purchase(purchase)
    rr.claim(claim)
    rr.freeup(freeup)
    rr.died(died)
    rr.cores = cores
    rr.socket = socket
    rr.power_watts = power_watts
    assert repr(rr) == expected


def test_namedtuple_fields_cpu() -> None:
    expected_fields = ("core", "socket", "power_watts")
    r = CPU(name="Intel-core", manufacturer="Intel")
    rr = eval(str(r))
    assert rr._nt_cpu()._fields == expected_fields


# ----------------------------- testing how faker package works in testing -----------------------------
def test_name_and_manufacturer_with_faker_cpu(fake) -> None:
    d = [
        {"cpu": fake.word().capitalize() + " CPU", "manufacturer": fake.company()}
        for _ in range(100)
    ]
    for dictionary in d:
        r = CPU(dictionary["cpu"], dictionary["manufacturer"])
        with check:
            assert r.name == dictionary["cpu"]
        with check:
            assert r.manufacturer == dictionary["manufacturer"]


# ------------------Test exceptions raised and text of exception correct-----------------------
"""Medium Level Test - test the program runs correctly
given the wrong input information."""


def test_raise_type_exception_should_pass_easy_cpu() -> None:
    """test that will catch TypeError exception when it is risen
    and test that the text of the exception is correct"""
    with pytest.raises(TypeError) as e:
        CPU("Intel-core", 1)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [
        (r, "Intel")
        for r in [
            [1, 2, 3],
            1,
            2j + 1,
            0.1,
            -0.5,
            int,
            str,
            float,
            complex,
            list,
            tuple,
            range,
            dict,
            set,
            frozenset,
        ]
    ],
)
def test_raise_type_exception_should_pass_parameterize_name_cpu(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        CPU(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [
        ("Intel-core", r)
        for r in [
            [1, 2, 3],
            1,
            2j + 1,
            0.1,
            -0.5,
            int,
            str,
            float,
            complex,
            list,
            tuple,
            range,
            dict,
            set,
            frozenset,
        ]
    ],
)
def test_raise_type_exception_should_pass_parameterize_manufacturer_cpu(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        CPU(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [(r, "Intel") for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_name_cpu(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        CPU(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [("Intel-core", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_manufacturer_cpu(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        CPU(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [
        ("Intel-core", "Intel", r)
        for r in [
            [1, 2, 3],
            2j + 1,
            0.1,
            -0.5,
            int,
            str,
            float,
            complex,
            list,
            tuple,
            range,
            dict,
            set,
            frozenset,
        ]
    ],
)
def test_raise_type_exception_should_pass_parameterize_integer_cpu(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(TypeError) as e:
        r = CPU(name, manufacturer)
        r.purchase(number)
    assert "Unsupported type for value, value must be a integer." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("Intel-core", "Intel", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_integer_cpu(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = CPU(name, manufacturer)
        r.purchase(number)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("Intel-core", "Intel", r) for r in [i for i in range(-10, 1)]],
)
def test_raise_value_exception_should_pass_parameterize_integer_is_negative_cpu(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = CPU(name, manufacturer)
        r.purchase(number)
    assert "Value must be greater than zero." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim",
    [("Intel-core", "Intel", p, 10) for p in [i for i in range(1, 10)]],
)
def test_raise_value_exception_should_pass_parameterize_claim_cpu(
    name: str, manufacturer: str, purchase: int, claim: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = CPU(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
    assert "The claimed number cannot be greater than total number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, freeup",
    [("Intel-core", "Intel", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_freeup_cpu(
    name: str, manufacturer: str, purchase: int, claim: int, freeup: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = CPU(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.freeup(freeup)
    assert "Freeup number cannot be greater than allocated number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, died",
    [("Intel-core", "Intel", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_died_cpu(
    name: str, manufacturer: str, purchase: int, claim: int, died: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = CPU(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.died(died)
    assert "The died number is greater than allocated number." == str(e.value)


# ------------- Extra tests -----------------------------
# ----------- test class, function, property types ------
def test_resource_is_instance_of_type_cpu() -> None:
    assert isinstance(CPU, type)


# --test that Mod class has 10 attributes --
def test_instance_has_13_property_attrs_cpu() -> None:
    """Test that class has 13 attrs
    ['allocated',
    'category',
    'claim',
    'cores',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'purchase',
    'power_watts',
    'remaining',
    'socket',
    'total']"""
    m = CPU(name="Intel-core", manufacturer="Intel")
    actual = len([attr for attr in dir(m) if not attr.startswith("_")])
    expected = 13
    assert (
        actual == expected
    ), f"{type(m).__name__} class does not have {expected} attributes."


def test_instance_has_13_attributes_cpu() -> None:
    """Test that class has 10 attrs
    ['allocated',
    'category',
    'claim',
    'cores',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'power_watts',
    'purchase',
    'remaining',
    'socket',
    'total']"""
    m = CPU(name="Intel-core", manufacturer="Intel")
    attributes = [attr for attr in dir(m) if not attr.startswith("_")]
    for attr in attributes:
        msg = f"The CPU instance does not have a {attr} attribute."
        assert hasattr(m, attr), msg


def test_if_three_attributes_properties_belong_to_class_cpu() -> None:
    """Test that 3 attrs belongs to class
    ['cores',
    'power_watts',
    'socket']"""
    m = CPU(name="Intel-core", manufacturer="Intel")
    attributes = ["cores", "socket", "power_watts"]
    for attr in attributes:
        msg = f"{attr} attribute is not in instance scope."
        with check:
            assert attr in CPU.__dict__, msg
        with check:
            assert attr in type(m).__dict__, msg
        with check:
            assert attr in m.__class__.__dict__, msg
        # assert attr in m.__dict__, msg


def test_if_eight_private_attributes_belong_to_instance_cpu() -> None:
    """Test that instance dictionary has 8 private attrs
    {'_name': 'Intel-core',
    '_manufacturer': 'Intel',
    '  _total': 0,
    '_allocated': 0,
    '_remaining': 0,
    '_cores': None,
    '_socket': None,
    '_power_watts': None}"""
    m = CPU(name="Intel-core", manufacturer="Intel")
    repr(m)  # need to call installs to create _remaining attr
    with check:
        assert "_name" in m.__dict__
    with check:
        assert "_manufacturer" in m.__dict__
    with check:
        assert "_total" in m.__dict__
    with check:
        assert "_allocated" in m.__dict__
    with check:
        assert "_remaining" in m.__dict__
    with check:
        assert "_cores" in m.__dict__
    with check:
        assert "_socket" in m.__dict__
    with check:
        assert "_power_watts" in m.__dict__


def test_instance_has_8_attributes_cpu() -> None:
    m = CPU(name="Intel-core", manufacturer="Intel")
    repr(m)  # need to call installs to create _remaining attr
    attributes = [
        "_name",
        "_manufacturer",
        "_total",
        "_allocated",
        "_remaining",
        "_cores",
        "_socket",
        "_power_watts",
    ]
    for attr in attributes:
        msg = f"The CPU instance does not have {attr} attribute."
        assert hasattr(m, attr), msg


def test_name_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.name, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "name"), property)


def test_manufacturer_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.manufacturer, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "manufacturer"), property)


def test_total_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.total, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "total"), property)


def test_allocated_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.allocated, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "allocated"), property)


def test_remaining_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.remaining, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "remaining"), property)


def test_category_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.category, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "category"), property)


def test_cores_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.cores, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "cores"), property)


def test_socket_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.socket, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "socket"), property)


def test_power_watts_is_property_cpu() -> None:
    with check:
        assert isinstance(CPU.power_watts, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(CPU, "power_watts"), property)


def test_validate_str_is_function_cpu() -> None:
    """In child class _validate_str is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU._validate_str,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "_validate_str"),
            types.FunctionType,
        )


def test_validate_int_is_function_cpu() -> None:
    """In child class _validate_int is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU._validate_int,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "_validate_int"),
            types.FunctionType,
        )


def test_nt_cpu_is_function_cpu() -> None:
    with check:
        assert isinstance(
            CPU.__dict__["_nt_cpu"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "_nt_cpu"),
            types.FunctionType,
        )


def test_nt_resource_is_function_cpu() -> None:
    """In child class _nt_resource is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU._nt_resource,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "_nt_resource"),
            types.FunctionType,
        )


def test_purchase_is_function_cpu() -> None:
    """In child class purchase is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU.purchase,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "purchase"),
            types.FunctionType,
        )


def test_claim_is_function_cpu() -> None:
    """In child class claim is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU.claim,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "claim"),
            types.FunctionType,
        )


def test_freeup_is_function_cpu() -> None:
    """In child class freeup is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU.freeup,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "freeup"),
            types.FunctionType,
        )


def test_died_is_function_of_cpu() -> None:
    """In child class died is not in class or instance dictionary"""
    with check:
        assert isinstance(
            CPU.died,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(CPU, "died"),
            types.FunctionType,
        )


def test_purchase_is_callable_cpu() -> None:
    assert callable(CPU.purchase), f"'purchase' is not callable."


def test_attributes_name_manufacturer_total_allocated_remaining_are_not_callable_cpu() -> (
    None
):
    with check:
        assert not callable(CPU.name), f"'name' is callable."
    with check:
        assert not callable(CPU.manufacturer), f"'manufacturer' is callable."
    with check:
        assert not callable(CPU.total), f"'total' is callable."
    with check:
        assert not callable(CPU.allocated), f"'allocated' is callable."
    with check:
        assert not callable(CPU.remaining), f"'remaining' is callable."
