import pytest
from inventory_application.apps.sdd import SDD
from pytest_check import check
import inspect
import types


# --------in case I want to apply the same marker for all below pytest use below. xyz is the name of the marker:-----
# It is a modular fixture. This means that every test function in this file after `pytestmark = pytest.mark.xyz` will
# have this decorator.
# pytestmark = pytest.mark.xyz or pytestmark = [pytest.mark.xyz, pytest.mark.abc]
pytestmark = pytest.mark.sdd

# to test specific test write: $ pytest -k name_of_the_test

# to check coverage: $ coverage run -m pytest .
# generate coverage report: $ coverage html

# ----------------------- Easy level tests: test SDD with different values ----


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("A400 SATA", "Kingston", "A400 SATA", "Kingston"),
        ("Barracuda", "Seagate", "Barracuda", "Seagate"),
        ("KC3000", "Kingston", "KC3000", "Kingston"),
    ],
)
def test_name_manufacturer_sdd(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    with check:
        assert r.name == expected_name
    with check:
        assert r.manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("A400 SATA", "Kingston", "A400 SATA", "Kingston"),
        ("Barracuda", "Seagate", "Barracuda", "Seagate"),
        ("KC3000", "Kingston", "KC3000", "Kingston"),
    ],
)
def test_private_name_manufacture_sdd(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    with check:
        assert r._name == expected_name
    with check:
        assert r._manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, interface, expected_interface",
    [
        ("A400 SATA", "Kingston", "A400 3.0 x4", "A400 3.0 x4"),
        ("Barracuda", "Seagate", "PCIe", "PCIe"),
        (
            "KC3000",
            "Kingston",
            "PCIe 4.0 NVMe",
            "PCIe 4.0 NVMe",
        ),
    ],
)
def test_setter_for_interface_sdd(
    name: str, manufacturer: str, interface: str, expected_interface: str
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    with check:
        r.interface = interface
        assert r.interface == expected_interface


@pytest.mark.parametrize(
    "name, manufacturer, capacity_GB, expected_capacity_GB",
    [
        ("A400 SATA", "Kingston", 200, 200),
        ("Barracuda", "Seagate", 300, 300),
        ("KC3000", "Kingston", 500, 500),
    ],
)
def test_setter_for_capacity_gb_sdd(
    name: str, manufacturer: str, capacity_GB: int, expected_capacity_GB: int
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    with check:
        r.capacity_GB = capacity_GB
        assert r.capacity_GB == expected_capacity_GB


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, interface, expected",
    [
        (
            "A400 SATA",
            "Kingston",
            7,
            3,
            1,
            1,
            120,
            "A400 3.0 x4",
            dict(
                category="sdd",
                name="A400 SATA",
                manufacturer="Kingston",
                total=6,
                allocated=1,
                remaining=5,
                capacity_GB=120,
                interface="A400 3.0 x4",
            ),
        ),
        (
            "Barracuda",
            "Seagate",
            10,
            4,
            3,
            1,
            200,
            "PCIe",
            dict(
                category="sdd",
                name="Barracuda",
                manufacturer="Seagate",
                total=9,
                allocated=0,
                remaining=9,
                capacity_GB=200,
                interface="PCIe",
            ),
        ),
        (
            "KC3000",
            "Kingston",
            10,
            7,
            5,
            1,
            500,
            "PCIe 4.0 NVMe",
            dict(
                category="sdd",
                name="KC3000",
                manufacturer="Kingston",
                total=9,
                allocated=1,
                remaining=8,
                capacity_GB=500,
                interface="PCIe 4.0 NVMe",
            ),
        ),
    ],
)
def test_total_allocated_remaining_category_capacity_gb_interface_property_sdd(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    interface: str,
    expected: dict,
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    r.interface = interface
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
        assert r.interface == expected["interface"]


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, interface, expected",
    [
        (
            "A400 SATA",
            "Kingston",
            7,
            3,
            1,
            1,
            120,
            "A400 3.0 x4",
            "SDD(category='sdd', name='A400 SATA', manufacturer='Kingston', total=6, allocated=1, remaining=5, capacity_GB=120, interface='A400 3.0 x4')",
        ),
        (
            "Barracuda",
            "Seagate",
            10,
            4,
            3,
            1,
            200,
            "PCIe",
            "SDD(category='sdd', name='Barracuda', manufacturer='Seagate', total=9, allocated=0, remaining=9, capacity_GB=200, interface='PCIe')",
        ),
        (
            "KC3000",
            "Kingston",
            10,
            7,
            5,
            1,
            500,
            "PCIe 4.0 NVMe",
            "SDD(category='sdd', name='KC3000', manufacturer='Kingston', total=9, allocated=1, remaining=8, capacity_GB=500, interface='PCIe 4.0 NVMe')",
        ),
    ],
)
def test_repr_method_v1_sdd(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    interface: str,
    expected: str,
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    r.interface = interface
    assert repr(r) == expected


def test_repr_method_v2_sdd(repr_fixt_sdd) -> None:
    (
        name,
        manufacturer,
        purchase,
        claim,
        freeup,
        died,
        capacity_GB,
        interface,
        expected,
    ) = repr_fixt_sdd
    r = SDD(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    r.interface = interface
    assert repr(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, expected",
    [
        (
            "A400 SATA",
            "Kingston",
            "SDD(name='A400 SATA', manufacturer='Kingston')",
        ),
        (
            "Barracuda",
            "Seagate",
            "SDD(name='Barracuda', manufacturer='Seagate')",
        ),
        (
            "KC3000",
            "Kingston",
            "SDD(name='KC3000', manufacturer='Kingston')",
        ),
    ],
)
def test_str_method_v1_sdd(
    name: str,
    manufacturer: str,
    expected: str,
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    assert str(r) == expected


def test_str_method_v2_sdd(str_fixt_sdd) -> None:
    name, manufacturer, expected = str_fixt_sdd
    r = SDD(name=name, manufacturer=manufacturer)
    assert str(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, interface, expected",
    [
        (
            "A400 SATA",
            "Kingston",
            7,
            3,
            1,
            1,
            120,
            "A400 3.0 x4",
            "SDD(category='sdd', name='A400 SATA', manufacturer='Kingston', total=6, allocated=1, remaining=5, capacity_GB=120, interface='A400 3.0 x4')",
        ),
        (
            "Barracuda",
            "Seagate",
            10,
            4,
            3,
            1,
            200,
            "PCIe",
            "SDD(category='sdd', name='Barracuda', manufacturer='Seagate', total=9, allocated=0, remaining=9, capacity_GB=200, interface='PCIe')",
        ),
        (
            "KC3000",
            "Kingston",
            10,
            7,
            5,
            1,
            500,
            "PCIe 4.0 NVMe",
            "SDD(category='sdd', name='KC3000', manufacturer='Kingston', total=9, allocated=1, remaining=8, capacity_GB=500, interface='PCIe 4.0 NVMe')",
        ),
    ],
)
def test_convert_str_to_instance_sdd(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    interface: str,
    expected: str,
) -> None:
    r = SDD(name=name, manufacturer=manufacturer)
    rr = eval(str(r))
    rr.purchase(purchase)
    rr.claim(claim)
    rr.freeup(freeup)
    rr.died(died)
    rr.capacity_GB = capacity_GB
    rr.interface = interface
    assert repr(rr) == expected


def test_namedtuple_fields_sdd() -> None:
    expected_fields = ("interface",)
    r = SDD(name="A400 SATA", manufacturer="Kingston")
    rr = eval(str(r))
    assert rr._nt_sdd()._fields == expected_fields


# ----------------------------- testing how faker package works in testing -----------------------------
def test_name_and_manufacturer_with_faker_sdd(fake) -> None:
    d = [
        {
            "SDD": fake.word().capitalize() + " SDD",
            "manufacturer": fake.company(),
        }
        for _ in range(100)
    ]
    for dictionary in d:
        r = SDD(dictionary["SDD"], dictionary["manufacturer"])
        with check:
            assert r.name == dictionary["SDD"]
        with check:
            assert r.manufacturer == dictionary["manufacturer"]


# ------------------Test exceptions raised and text of exception correct-----------------------
"""Medium Level Test - test the program runs correctly
given the wrong input information."""


def test_raise_type_exception_should_pass_easy_sdd() -> None:
    """test that will catch TypeError exception when it is risen
    and test that the text of the exception is correct"""
    with pytest.raises(TypeError) as e:
        SDD("A400 SATA", 1)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [
        (r, "Kingston")
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
def test_raise_type_exception_should_pass_parameterize_name_sdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        SDD(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [
        ("A400 SATA", r)
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
def test_raise_type_exception_should_pass_parameterize_manufacturer_sdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        SDD(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [(r, "Kingston") for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_name_sdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        SDD(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [("A400 SATA", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_manufacturer_sdd(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        SDD(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, interface",
    [("A400 SATA", "Kingston", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_inteface_none_sdd(
    name: str, manufacturer: str, interface: int
) -> None:
    with pytest.raises(ValueError) as e:
        sdd = SDD(name, manufacturer)
        sdd.interface = interface
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [
        ("A400 SATA", "Kingston", r)
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
def test_raise_type_exception_should_pass_parameterize_integer_sdd(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(TypeError) as e:
        r = SDD(name, manufacturer)
        r.purchase(number)
    assert "Unsupported type for value, value must be a integer." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, interface",
    [
        ("A400 SATA", "Kingston", r)
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
def test_raise_type_exception_should_pass_parameterize_integer_interface_sdd(
    name: str, manufacturer: str, interface: str
) -> None:
    with pytest.raises(TypeError) as e:
        r = SDD(name, manufacturer)
        r.interface = interface
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("A400 SATA", "Kingston", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_integer_sdd(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = SDD(name, manufacturer)
        r.purchase(number)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("A400 SATA", "Kingston", r) for r in [i for i in range(-10, 1)]],
)
def test_raise_value_exception_should_pass_parameterize_integer_is_negative_sdd(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = SDD(name, manufacturer)
        r.purchase(number)
    assert "Value must be greater than zero." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim",
    [("A400 SATA", "Kingston", p, 10) for p in [i for i in range(1, 10)]],
)
def test_raise_value_exception_should_pass_parameterize_claim_sdd(
    name: str, manufacturer: str, purchase: int, claim: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = SDD(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
    assert "The claimed number cannot be greater than total number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, freeup",
    [("A400 SATA", "Kingston", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_freeup_sdd(
    name: str, manufacturer: str, purchase: int, claim: int, freeup: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = SDD(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.freeup(freeup)
    assert "Freeup number cannot be greater than allocated number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, died",
    [("A400 SATA", "Kingston", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_died_sdd(
    name: str, manufacturer: str, purchase: int, claim: int, died: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = SDD(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.died(died)
    assert "The died number is greater than allocated number." == str(e.value)


# ------------- Extra tests -----------------------------
# ----------- test class, function, property types ------
def test_resource_is_instance_of_type_sdd() -> None:
    assert isinstance(SDD, type)


# --test that SDD class has 10 attributes --
def test_instance_has_12_property_attrs_sdd() -> None:
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
    'interface',
    'total']"""
    m = SDD(name="A400 SATA", manufacturer="Kingston")
    actual = len([attr for attr in dir(m) if not attr.startswith("_")])
    expected = 12
    assert (
        actual == expected
    ), f"{type(m).__name__} class does not have {expected} attributes."


def test_instance_has_12_attributes_sdd() -> None:
    """Test that class has 10 attrs
    ['allocated',
    'capacity_GB',
    'category',
    'claim',
    'died',
    'freeup',
    'interface',
    'manufacturer',
    'name',
    'purchase',
    'remaining',
    'total']"""
    m = SDD(name="A400 SATA", manufacturer="Kingston")
    attributes = [attr for attr in dir(m) if not attr.startswith("_")]
    for attr in attributes:
        msg = f"The SDD instance does not have a {attr} attribute."
        assert hasattr(m, attr), msg


def test_if_one_attribute_property_belong_to_class_sdd() -> None:
    """Test that 2 attribute belongs to class
    ['capacity_GB']"""
    m = SDD(name="A400 SATA", manufacturer="Kingston")
    attributes = ["interface"]
    for attr in attributes:
        msg = f"{attr} attribute is not in instance scope."
        with check:
            assert attr in SDD.__dict__, msg
        with check:
            assert attr in type(m).__dict__, msg
        with check:
            assert attr in m.__class__.__dict__, msg
        # assert attr in m.__dict__, msg


def test_if_7_private_attributes_belong_to_instance_SDD() -> None:
    """Test that instance dictionary has 5 private attrs
    {'_name': 'SkyHawk',
    '_manufacturer': 'Seagate',
    '_total': 0,
    '_allocated': 0,
    '_capacity_GB': None,
    '_interface': None,
    '_remaining': 0}"""
    m = SDD(name="A400 SATA", manufacturer="Kingston")
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
        assert "_interface" in m.__dict__
    with check:
        assert "_capacity_GB" in m.__dict__


def test_instance_has__7_attributes_sdd() -> None:
    m = SDD(name="A400 SATA", manufacturer="Kingston")
    repr(m)  # need to call installs to create _remaining attr
    attributes = [
        "_name",
        "_manufacturer",
        "_total",
        "_allocated",
        "_remaining",
        "_capacity_GB",
        "_interface",
    ]
    for attr in attributes:
        msg = f"The SDD instance does not have {attr} attribute."
        assert hasattr(m, attr), msg


def test_name_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.name, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "name"), property)


def test_manufacturer_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.manufacturer, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "manufacturer"), property)


def test_total_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.total, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "total"), property)


def test_allocated_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.allocated, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "allocated"), property)


def test_remaining_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.remaining, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "remaining"), property)


def test_category_is_property_SDD() -> None:
    with check:
        assert isinstance(SDD.category, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "category"), property)


def test_capacity_gb_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.capacity_GB, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "capacity_GB"), property)


def test_interface_is_property_sdd() -> None:
    with check:
        assert isinstance(SDD.interface, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(SDD, "interface"), property)


def test_validate_str_is_function_sdd() -> None:
    """In child class _validate_str is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD._validate_str,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "_validate_str"),
            types.FunctionType,
        )


def test_validate_int_is_function_sdd() -> None:
    """In child class _validate_int is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD._validate_int,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "_validate_int"),
            types.FunctionType,
        )


def test_nt_sdd_is_function_sdd() -> None:
    with check:
        assert isinstance(
            SDD.__dict__["_nt_sdd"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "_nt_sdd"),
            types.FunctionType,
        )


def test_nt_resource_is_function_sdd() -> None:
    """In child class _nt_resource is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD._nt_resource,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "_nt_resource"),
            types.FunctionType,
        )


def test_purchase_is_function_sdd() -> None:
    """In child class purchase is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD.purchase,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "purchase"),
            types.FunctionType,
        )


def test_claim_is_function_sdd() -> None:
    """In child class claim is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD.claim,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "claim"),
            types.FunctionType,
        )


def test_freeup_is_function_sdd() -> None:
    """In child class freeup is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD.freeup,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "freeup"),
            types.FunctionType,
        )


def test_died_is_function_of_sdd() -> None:
    """In child class died is not in class or instance dictionary"""
    with check:
        assert isinstance(
            SDD.died,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(SDD, "died"),
            types.FunctionType,
        )


def test_purchase_is_callable_sdd() -> None:
    assert callable(SDD.purchase), f"'purchase' is not callable."


def test_attributes_name_manufacturer_total_allocated_remaining_are_not_callable_sdd() -> (
    None
):
    with check:
        assert not callable(SDD.name), f"'name' is callable."
    with check:
        assert not callable(SDD.manufacturer), f"'manufacturer' is callable."
    with check:
        assert not callable(SDD.total), f"'total' is callable."
    with check:
        assert not callable(SDD.allocated), f"'allocated' is callable."
    with check:
        assert not callable(SDD.remaining), f"'remaining' is callable."
