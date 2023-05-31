import pytest
from inventory_application.apps.hdd import HDD
from pytest_check import check
import inspect
import types


# --------in case I want to apply the same marker for all below pytest use below. xyz is the name of the marker:-----
# It is a modular fixture. This means that every test function in this file after `pytestmark = pytest.mark.xyz` will
# have this decorator.
# pytestmark = pytest.mark.xyz or pytestmark = [pytest.mark.xyz, pytest.mark.abc]
pytestmark = pytest.mark.hdd

# to test specific test write: $ pytest -k name_of_the_test

# to check coverage: $ coverage run -m pytest .
# generate coverage report: $ coverage html

# ----------------------- Easy level tests: test HDD with different values ----


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("SkyHawk", "Seagate", "SkyHawk", "Seagate"),
        ("WD Blue", "WD", "WD Blue", "WD"),
        ("Barracuda", "Seagate", "Barracuda", "Seagate"),
    ],
)
def test_name_manufacturer_hdd(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    with check:
        assert r.name == expected_name
    with check:
        assert r.manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("SkyHawk", "Seagate", "SkyHawk", "Seagate"),
        ("WD Blue", "WD", "WD Blue", "WD"),
        ("Barracuda", "Seagate", "Barracuda", "Seagate"),
    ],
)
def test_private_name_manufacture_hdd(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    with check:
        assert r._name == expected_name
    with check:
        assert r._manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, size, new_size, expected_size, expected_new_size",
    [
        (
            "SkyHawk",
            "Seagate",
            '2.5"',
            '3.5"',
            '2.5"',
            '3.5"',
        ),
        ("WD Blue", "WD", '2.5"', '3.5"', '2.5"', '3.5"'),
        (
            "Barracuda",
            "Seagate",
            '3.5"',
            '2.5"',
            '3.5"',
            '2.5"',
        ),
    ],
)
def test_setter_for_size_hdd(
    name: str,
    manufacturer: str,
    size: str,
    new_size: str,
    expected_size: str,
    expected_new_size: str,
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    with check:
        r.size = size
        assert r.size == expected_size
    with check:
        r.size = new_size
        assert r.size == expected_new_size


@pytest.mark.parametrize(
    "name, manufacturer, rpm, new_rpm, expected_rpm, expected_new_rpm",
    [
        (
            "SkyHawk",
            "Seagate",
            5400,
            10_000,
            5400,
            10_000,
        ),
        ("WD Blue", "WD", 7000, 8000, 7000, 8000),
        (
            "Barracuda",
            "Seagate",
            10_000,
            9000,
            10_000,
            9000,
        ),
    ],
)
def test_setter_for_rpm_hdd(
    name: str,
    manufacturer: str,
    rpm: int,
    new_rpm: int,
    expected_rpm: int,
    expected_new_rpm: int,
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    with check:
        r.rpm = rpm
        assert r.rpm == expected_rpm
    with check:
        r.rpm = new_rpm
        assert r.rpm == expected_new_rpm


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, size, rpm, expected",
    [
        (
            "SkyHawk",
            "Seagate",
            7,
            3,
            1,
            1,
            120,
            '2.5"',
            5400,
            dict(
                category="hdd",
                name="SkyHawk",
                manufacturer="Seagate",
                total=6,
                allocated=1,
                remaining=5,
                capacity_GB=120,
                size='2.5"',
                rpm=5400,
            ),
        ),
        (
            "WD Blue",
            "WD",
            10,
            4,
            3,
            1,
            200,
            '3.5"',
            7000,
            dict(
                category="hdd",
                name="WD Blue",
                manufacturer="WD",
                total=9,
                allocated=0,
                remaining=9,
                capacity_GB=200,
                size='3.5"',
                rpm=7000,
            ),
        ),
        (
            "Barracuda",
            "Seagate",
            10,
            7,
            5,
            1,
            500,
            '2.5"',
            10_000,
            dict(
                category="hdd",
                name="Barracuda",
                manufacturer="Seagate",
                total=9,
                allocated=1,
                remaining=8,
                capacity_GB=500,
                size='2.5"',
                rpm=10_000,
            ),
        ),
    ],
)
def test_total_allocated_remaining_category_capacity_gb_size_rpm_property_hdd(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    size: str,
    rpm: int,
    expected: dict,
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    r.size = size
    r.rpm = rpm
    with check:
        assert r.total == expected["total"]
    with check:
        assert r.allocated == expected["allocated"]
    with check:
        assert r.remaining == expected["remaining"]
    with check:
        assert r.category == expected["category"]
    with check:
        assert r.capacity_GB == expected["capacity_GB"]
    with check:
        assert r.size == expected["size"]
    with check:
        assert r.rpm == expected["rpm"]


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, size, rpm, expected",
    [
        (
            "SkyHawk",
            "Seagate",
            7,
            3,
            1,
            1,
            120,
            '2.5"',
            5400,
            "HDD(category='hdd', name='SkyHawk', manufacturer='Seagate', total=6, allocated=1, remaining=5, capacity_GB=120, size='2.5\"', rpm=5400)",
        ),
        (
            "WD Blue",
            "WD",
            10,
            4,
            3,
            1,
            200,
            '3.5"',
            7000,
            "HDD(category='hdd', name='WD Blue', manufacturer='WD', total=9, allocated=0, remaining=9, capacity_GB=200, size='3.5\"', rpm=7000)",
        ),
        (
            "Barracuda",
            "Seagate",
            10,
            7,
            5,
            1,
            500,
            '2.5"',
            10000,
            "HDD(category='hdd', name='Barracuda', manufacturer='Seagate', total=9, allocated=1, remaining=8, capacity_GB=500, size='2.5\"', rpm=10000)",
        ),
    ],
)
def test_repr_method_v1_hdd(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    size: str,
    rpm: int,
    expected: str,
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    r.size = size
    r.rpm = rpm
    assert repr(r) == expected


def test_repr_method_v2_hdd(repr_fixt_hdd) -> None:
    (
        name,
        manufacturer,
        purchase,
        claim,
        freeup,
        died,
        capacity_GB,
        size,
        rpm,
        expected,
    ) = repr_fixt_hdd
    r = HDD(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    r.size = size
    r.rpm = rpm
    assert repr(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, expected",
    [
        (
            "SkyHawk",
            "Seagate",
            "HDD(name='SkyHawk', manufacturer='Seagate')",
        ),
        (
            "WD Blue",
            "WD",
            "HDD(name='WD Blue', manufacturer='WD')",
        ),
        (
            "Barracuda",
            "Seagate",
            "HDD(name='Barracuda', manufacturer='Seagate')",
        ),
    ],
)
def test_str_method_v1_hdd(
    name: str,
    manufacturer: str,
    expected: str,
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    assert str(r) == expected


def test_str_method_v2_hdd(str_fixt_hdd) -> None:
    name, manufacturer, expected = str_fixt_hdd
    r = HDD(name=name, manufacturer=manufacturer)
    assert str(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, size, rpm, expected",
    [
        (
            "SkyHawk",
            "Seagate",
            7,
            3,
            1,
            1,
            120,
            '2.5"',
            5400,
            "HDD(category='hdd', name='SkyHawk', manufacturer='Seagate', total=6, allocated=1, remaining=5, capacity_GB=120, size='2.5\"', rpm=5400)",
        ),
        (
            "WD Blue",
            "WD",
            10,
            4,
            3,
            1,
            200,
            '3.5"',
            7000,
            "HDD(category='hdd', name='WD Blue', manufacturer='WD', total=9, allocated=0, remaining=9, capacity_GB=200, size='3.5\"', rpm=7000)",
        ),
        (
            "Barracuda",
            "Seagate",
            10,
            7,
            5,
            1,
            500,
            '2.5"',
            10000,
            "HDD(category='hdd', name='Barracuda', manufacturer='Seagate', total=9, allocated=1, remaining=8, capacity_GB=500, size='2.5\"', rpm=10000)",
        ),
    ],
)
def test_convert_str_to_instance_hdd(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    size: str,
    rpm: int,
    expected: str,
) -> None:
    r = HDD(name=name, manufacturer=manufacturer)
    rr = eval(str(r))
    rr.purchase(purchase)
    rr.claim(claim)
    rr.freeup(freeup)
    rr.died(died)
    rr.capacity_GB = capacity_GB
    rr.size = size
    rr.rpm = rpm
    assert repr(rr) == expected


def test_namedtuple_fields_hdd() -> None:
    expected_fields = ("size", "rpm")
    r = HDD(name="SkyHawk", manufacturer="Seagate")
    rr = eval(str(r))
    assert rr._nt_hdd()._fields == expected_fields


# ----------------------------- testing how faker package works in testing -----------------------------
def test_name_and_manufacturer_with_faker_hdd(fake) -> None:
    d = [
        {
            "HDD": fake.word().capitalize() + " HDD",
            "manufacturer": fake.company(),
        }
        for _ in range(100)
    ]
    for dictionary in d:
        r = HDD(dictionary["HDD"], dictionary["manufacturer"])
        with check:
            assert r.name == dictionary["HDD"]
        with check:
            assert r.manufacturer == dictionary["manufacturer"]


# ------------------Test exceptions raised and text of exception correct-----------------------
"""Medium Level Test - test the program runs correctly
given the wrong input information."""


def test_raise_type_exception_should_pass_easy_hdd() -> None:
    """test that will catch TypeError exception when it is risen
    and test that the text of the exception is correct"""
    with pytest.raises(TypeError) as e:
        HDD("SkyHawk", 1)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [
        (r, "Seagate")
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
def test_raise_type_exception_should_pass_parameterize_name_hdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        HDD(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [
        ("SkyHawk", r)
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
def test_raise_type_exception_should_pass_parameterize_manufacturer_hdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        HDD(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [(r, "Seagate") for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_name_hdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        HDD(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [("SkyHawk", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_manufacturer_hdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        HDD(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, rpm",
    [("SkyHawk", "Seagate", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_rpm_none_hdd(
    name: str, manufacturer: str, rpm: int
) -> None:
    with pytest.raises(ValueError) as e:
        hdd = HDD(name, manufacturer)
        hdd.rpm = rpm
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, size",
    [("SkyHawk", "Seagate", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_size_none_hdd(
    name: str, manufacturer: str, size: int
) -> None:
    with pytest.raises(ValueError) as e:
        hdd = HDD(name, manufacturer)
        hdd.size = size
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [
        ("SkyHawk", "Seagate", r)
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
def test_raise_type_exception_should_pass_parameterize_integer_hdd(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(TypeError) as e:
        r = HDD(name, manufacturer)
        r.purchase(number)
    assert "Unsupported type for value, value must be a integer." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, rpm",
    [
        ("SkyHawk", "Seagate", r)
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
def test_raise_type_exception_should_pass_parameterize_integer_rpm_hdd(
    name: str, manufacturer: str, rpm: int
) -> None:
    with pytest.raises(TypeError) as e:
        r = HDD(name, manufacturer)
        r.rpm = rpm
    assert "Unsupported type for value, value must be a integer." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, size",
    [
        ("SkyHawk", "Seagate", r)
        for r in [
            [1, 2, 3],
            2j + 1,
            0.1,
            1,
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
def test_raise_type_exception_should_pass_parameterize_integer_size_hdd(
    name: str, manufacturer: str, size: str
) -> None:
    with pytest.raises(TypeError) as e:
        r = HDD(name, manufacturer)
        r.size = size
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("SkyHawk", "Seagate", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_integer_hdd(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.purchase(number)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("SkyHawk", "Seagate", r) for r in [i for i in range(-10, 1)]],
)
def test_raise_value_exception_should_pass_parameterize_integer_is_negative_hdd(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.purchase(number)
    assert "Value must be greater than zero." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, rpm",
    [("SkyHawk", "Seagate", r) for r in [i for i in range(-10, 1)]],
)
def test_raise_value_exception_should_pass_parameterize_integer_is_negative_rpm_hdd(
    name: str, manufacturer: str, rpm: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.rpm = rpm
    assert "Value must be greater than zero." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim",
    [("SkyHawk", "Seagate", p, 10) for p in [i for i in range(1, 10)]],
)
def test_raise_value_exception_should_pass_parameterize_claim_hdd(
    name: str, manufacturer: str, purchase: int, claim: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
    assert "The claimed number cannot be greater than total number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, freeup",
    [("SkyHawk", "Seagate", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_freeup_hdd(
    name: str, manufacturer: str, purchase: int, claim: int, freeup: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.freeup(freeup)
    assert "Freeup number cannot be greater than allocated number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, died",
    [("SkyHawk", "Seagate", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_died_hdd(
    name: str, manufacturer: str, purchase: int, claim: int, died: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.died(died)
    assert "The died number is greater than allocated number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, rpm",
    [
        ("SkyHawk", "Seagate", f)
        for f in list(range(5_300, 5_400)) + list(range(10_001, 10_100))
    ],
)
def test_raise_value_exception_should_pass_parameterize_rpm_hdd(
    name: str, manufacturer: str, rpm: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.rpm = rpm
    assert "value can only be between 5,400 and 10,000." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, size",
    [("SkyHawk", "Seagate", r) for r in ['4.5"', "5"]],
)
def test_raise_value_exception_should_pass_parameterize_size_hdd(
    name: str, manufacturer: str, size: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = HDD(name, manufacturer)
        r.size = size
    assert 'value can be either 2.5" of 3.5" .' == str(e.value)


# ------------- Extra tests -----------------------------
# ----------- test class, function, property types ------
def test_resource_is_instance_of_type_hdd() -> None:
    assert isinstance(HDD, type)


# --test that HDD class has 10 attributes --
def test_instance_has_13_property_attrs_hdd() -> None:
    """Test that class has 13 attrs
    ['allocated',
    'capacity_GB',
    'category',
    'claim',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'purchase',
    'remaining',
    'rpm',
    'size',
    'total']"""
    m = HDD(name="SkyHawk", manufacturer="Seagate")
    actual = len([attr for attr in dir(m) if not attr.startswith("_")])
    expected = 13
    assert (
        actual == expected
    ), f"{type(m).__name__} class does not have {expected} attributes."


def test_instance_has_13_attributes_hdd() -> None:
    """Test that class has 10 attrs
    ['allocated',
    'capacity_GB'
    'category',
    'claim',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'purchase',
    'remaining',
    'total']"""
    m = HDD(name="SkyHawk", manufacturer="Seagate")
    attributes = [attr for attr in dir(m) if not attr.startswith("_")]
    for attr in attributes:
        msg = f"The HDD instance does not have a {attr} attribute."
        assert hasattr(m, attr), msg


def test_if_two_attribute_property_belong_to_class_hdd() -> None:
    """Test that 2 attribute belongs to class
    ['capacity_GB']"""
    m = HDD(name="SkyHawk", manufacturer="Seagate")
    attributes = ["size", "rpm"]
    for attr in attributes:
        msg = f"{attr} attribute is not in instance scope."
        with check:
            assert attr in HDD.__dict__, msg
        with check:
            assert attr in type(m).__dict__, msg
        with check:
            assert attr in m.__class__.__dict__, msg
        # assert attr in m.__dict__, msg


def test_if_8_private_attributes_belong_to_instance_hdd() -> None:
    """Test that instance dictionary has 5 private attrs
    {'_name': 'SkyHawk',
    '_manufacturer': 'Seagate',
    '_total': 0,
    '_allocated': 0,
    '_capacity_GB': None,
    '_size': None,
    '_rpm': None,
    '_remaining': 0}"""
    m = HDD(name="SkyHawk", manufacturer="Seagate")
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
        assert "_size" in m.__dict__
    with check:
        assert "_rpm" in m.__dict__
    with check:
        assert "_capacity_GB" in m.__dict__


def test_instance_has__8_attributes_hdd() -> None:
    m = HDD(name="SkyHawk", manufacturer="Seagate")
    repr(m)  # need to call installs to create _remaining attr
    attributes = [
        "_name",
        "_manufacturer",
        "_total",
        "_allocated",
        "_remaining",
        "_capacity_GB",
        "_size",
        "_rpm",
    ]
    for attr in attributes:
        msg = f"The HDD instance does not have {attr} attribute."
        assert hasattr(m, attr), msg


def test_name_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.name, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "name"), property)


def test_manufacturer_is_property_HDD() -> None:
    with check:
        assert isinstance(HDD.manufacturer, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "manufacturer"), property)


def test_total_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.total, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "total"), property)


def test_allocated_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.allocated, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "allocated"), property)


def test_remaining_is_property_HDD() -> None:
    with check:
        assert isinstance(HDD.remaining, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "remaining"), property)


def test_category_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.category, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "category"), property)


def test_capacity_gb_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.capacity_GB, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "capacity_GB"), property)


def test_size_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.size, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "size"), property)


def test_rpm_is_property_hdd() -> None:
    with check:
        assert isinstance(HDD.rpm, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(HDD, "rpm"), property)


def test_validate_str_is_function_hdd() -> None:
    """In child class _validate_str is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD._validate_str,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "_validate_str"),
            types.FunctionType,
        )


def test_validate_int_is_function_hdd() -> None:
    """In child class _validate_int is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD._validate_int,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "_validate_int"),
            types.FunctionType,
        )


def test_nt_hdd_is_function_hdd() -> None:
    with check:
        assert isinstance(
            HDD.__dict__["_nt_hdd"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "_nt_hdd"),
            types.FunctionType,
        )


def test_nt_resource_is_function_hdd() -> None:
    """In child class _nt_resource is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD._nt_resource,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "_nt_resource"),
            types.FunctionType,
        )


def test_purchase_is_function_hdd() -> None:
    """In child class purchase is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD.purchase,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "purchase"),
            types.FunctionType,
        )


def test_claim_is_function_hdd() -> None:
    """In child class claim is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD.claim,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "claim"),
            types.FunctionType,
        )


def test_freeup_is_function_hdd() -> None:
    """In child class freeup is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD.freeup,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "freeup"),
            types.FunctionType,
        )


def test_died_is_function_of_hdd() -> None:
    """In child class died is not in class or instance dictionary"""
    with check:
        assert isinstance(
            HDD.died,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(HDD, "died"),
            types.FunctionType,
        )


def test_purchase_is_callable_hdd() -> None:
    assert callable(HDD.purchase), f"'purchase' is not callable."


def test_attributes_name_manufacturer_total_allocated_remaining_are_not_callable_hdd() -> (
    None
):
    with check:
        assert not callable(HDD.name), f"'name' is callable."
    with check:
        assert not callable(HDD.manufacturer), f"'manufacturer' is callable."
    with check:
        assert not callable(HDD.total), f"'total' is callable."
    with check:
        assert not callable(HDD.allocated), f"'allocated' is callable."
    with check:
        assert not callable(HDD.remaining), f"'remaining' is callable."
