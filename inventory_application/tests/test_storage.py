import pytest
from inventory_application.apps.storage import Storage
from pytest_check import check
import inspect
import types


# --------in case I want to apply the same marker for all below pytest use below. xyz is the name of the marker:-----
# It is a modular fixture. This means that every test function in this file after `pytestmark = pytest.mark.xyz` will
# have this decorator.
# pytestmark = pytest.mark.xyz or pytestmark = [pytest.mark.xyz, pytest.mark.abc]
pytestmark = pytest.mark.storage

# to test specific test write: $ pytest -k name_of_the_test

# to check coverage: $ coverage run -m pytest .
# generate coverage report: $ coverage html

# ----------------------- Easy level tests: test Storage with different values ----


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("Intel-core", "Intel", "Intel-core", "Intel"),
        ("AMD-i9", "AMD", "AMD-i9", "AMD"),
        ("Intel-Pentium", "Intel", "Intel-Pentium", "Intel"),
    ],
)
def test_name_manufacturer_storage(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
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
def test_private_name_manufacture_storage(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
    with check:
        assert r._name == expected_name
    with check:
        assert r._manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, capacity_gb, new_capacity_gb, expected_gb, expected_new_capacity_gb",
    [
        (
            "Intel-core",
            "Intel",
            120,
            200,
            120,
            200,
        ),
        ("AMD-i9", "AMD", 100, 50, 100, 50),
        (
            "Intel-Pentium",
            "Intel",
            300,
            200,
            300,
            200,
        ),
    ],
)
def test_setter_for_capacity_gb_storage(
    name: str,
    manufacturer: str,
    capacity_gb: int,
    new_capacity_gb: int,
    expected_gb: int,
    expected_new_capacity_gb: int,
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
    with check:
        r.capacity_GB = capacity_gb
        assert r.capacity_GB == expected_gb
    with check:
        r.capacity_GB = new_capacity_gb
        assert r.capacity_GB == expected_new_capacity_gb

@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_GB, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            120,
            dict(
                category="storage",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=6,
                allocated=1,
                remaining=5,
                capacity_GB=120
            ),
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            200,
            dict(
                category="storage",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=9,
                allocated=0,
                remaining=9,
                capacity_GB=200
            ),
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            500,
            dict(
                category="storage",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=9,
                allocated=1,
                remaining=8,
                capacity_GB=500
            ),
        ),
    ],
)
def test_total_allocated_remaining_category_capacity_gb_property_storage(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_GB: int,
    expected: dict
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
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


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_gb, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            200,
            "Storage(category='storage', name='Intel-core', manufacturer='Intel', total=6, allocated=1, remaining=5, capacity_GB=200)",
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            100,
            "Storage(category='storage', name='AMD-i9', manufacturer='AMD', total=9, allocated=0, remaining=9, capacity_GB=100)",
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            500,
            "Storage(category='storage', name='Intel-Pentium', manufacturer='Intel', total=9, allocated=1, remaining=8, capacity_GB=500)",
        ),
    ],
)
def test_repr_method_v1_storage(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    capacity_gb: int,
    expected: str,
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_gb
    assert repr(r) == expected


def test_repr_method_v2_storage(repr_fixt_storage) -> None:
    (
        name,
        manufacturer,
        purchase,
        claim,
        freeup,
        died,
        capacity_GB,
        expected,
    ) = repr_fixt_storage
    r = Storage(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    r.capacity_GB = capacity_GB
    assert repr(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, expected",
    [
        (
            "Intel-core",
            "Intel",
            "Storage(name='Intel-core', manufacturer='Intel')",
        ),
        (
            "AMD-i9",
            "AMD",
            "Storage(name='AMD-i9', manufacturer='AMD')",
        ),
        (
            "Intel-Pentium",
            "Intel",
            "Storage(name='Intel-Pentium', manufacturer='Intel')",
        ),
    ],
)
def test_str_method_v1_storage(
    name: str,
    manufacturer: str,
    expected: str,
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
    assert str(r) == expected


def test_str_method_v2_storage(str_fixt_storage) -> None:
    name, manufacturer, expected = str_fixt_storage
    r = Storage(name=name, manufacturer=manufacturer)
    assert str(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, capacity_gb, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            100,
            "Storage(category='storage', name='Intel-core', manufacturer='Intel', total=6, allocated=1, remaining=5, capacity_GB=100)",
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            200,
            "Storage(category='storage', name='AMD-i9', manufacturer='AMD', total=9, allocated=0, remaining=9, capacity_GB=200)",
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            300,
            "Storage(category='storage', name='Intel-Pentium', manufacturer='Intel', total=9, allocated=1, remaining=8, capacity_GB=300)",
        ),
    ],
)
def test_convert_str_to_instance_storage(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    expected: str,
    capacity_gb: int
) -> None:
    r = Storage(name=name, manufacturer=manufacturer)
    rr = eval(str(r))
    rr.purchase(purchase)
    rr.claim(claim)
    rr.freeup(freeup)
    rr.died(died)
    rr.capacity_GB = capacity_gb
    assert repr(rr) == expected


def test_namedtuple_fields_storage() -> None:
    expected_fields = ("capacity_GB",)
    r = Storage(name="Intel-core", manufacturer="Intel")
    rr = eval(str(r))
    assert rr._nt_storage()._fields == expected_fields


# ----------------------------- testing how faker package works in testing -----------------------------
def test_name_and_manufacturer_with_faker_storage(fake) -> None:
    d = [
        {"Storage": fake.word().capitalize() + " Storage", "manufacturer": fake.company()}
        for _ in range(100)
    ]
    for dictionary in d:
        r = Storage(dictionary["Storage"], dictionary["manufacturer"])
        with check:
            assert r.name == dictionary["Storage"]
        with check:
            assert r.manufacturer == dictionary["manufacturer"]


# ------------------Test exceptions raised and text of exception correct-----------------------
"""Medium Level Test - test the program runs correctly
given the wrong input information."""


def test_raise_type_exception_should_pass_easy_storage() -> None:
    """test that will catch TypeError exception when it is risen
    and test that the text of the exception is correct"""
    with pytest.raises(TypeError) as e:
        Storage("Intel-core", 1)
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
def test_raise_type_exception_should_pass_parameterize_name_storage(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        Storage(name, manufacturer)
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
def test_raise_type_exception_should_pass_parameterize_manufacturer_storage(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        Storage(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [(r, "Intel") for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_name_storage(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        Storage(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [("Intel-core", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_manufacturer_storage(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        Storage(name, manufacturer)
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
def test_raise_type_exception_should_pass_parameterize_integer_storage(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(TypeError) as e:
        r = Storage(name, manufacturer)
        r.purchase(number)
    assert "Unsupported type for value, value must be a integer." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("Intel-core", "Intel", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_integer_storage(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Storage(name, manufacturer)
        r.purchase(number)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("Intel-core", "Intel", r) for r in [i for i in range(-10, 1)]],
)
def test_raise_value_exception_should_pass_parameterize_integer_is_negative_storage(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Storage(name, manufacturer)
        r.purchase(number)
    assert "Value must be greater than zero." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim",
    [("Intel-core", "Intel", p, 10) for p in [i for i in range(1, 10)]],
)
def test_raise_value_exception_should_pass_parameterize_claim_storage(
    name: str, manufacturer: str, purchase: int, claim: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Storage(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
    assert "The claimed number cannot be greater than total number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, freeup",
    [("Intel-core", "Intel", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_freeup_storage(
    name: str, manufacturer: str, purchase: int, claim: int, freeup: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Storage(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.freeup(freeup)
    assert "Freeup number cannot be greater than allocated number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, died",
    [("Intel-core", "Intel", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_died_storage(
    name: str, manufacturer: str, purchase: int, claim: int, died: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Storage(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.died(died)
    assert "The died number is greater than allocated number." == str(e.value)


# ------------- Extra tests -----------------------------
# ----------- test class, function, property types ------
def test_resource_is_instance_of_type_storage() -> None:
    assert isinstance(Storage, type)


# --test that Mod class has 10 attributes --
def test_instance_has_11_property_attrs_storage() -> None:
    """Test that class has 13 attrs
    ['allocated',
    'category',
    'claim',
    'capacity_GB',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'purchase',
    'remaining',
    'total']"""
    m = Storage(name="Intel-core", manufacturer="Intel")
    actual = len([attr for attr in dir(m) if not attr.startswith("_")])
    expected = 11
    assert (
        actual == expected
    ), f"{type(m).__name__} class does not have {expected} attributes."


def test_instance_has_11_attributes_storage() -> None:
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
    m = Storage(name="Intel-core", manufacturer="Intel")
    attributes = [attr for attr in dir(m) if not attr.startswith("_")]
    for attr in attributes:
        msg = f"The Storage instance does not have a {attr} attribute."
        assert hasattr(m, attr), msg


def test_if_one_attribute_property_belong_to_class_storage() -> None:
    """Test that 1 attribute belongs to class
    ['capacity_GB']"""
    m = Storage(name="Intel-core", manufacturer="Intel")
    attributes = ["capacity_GB"]
    for attr in attributes:
        msg = f"{attr} attribute is not in instance scope."
        with check:
            assert attr in Storage.__dict__, msg
        with check:
            assert attr in type(m).__dict__, msg
        with check:
            assert attr in m.__class__.__dict__, msg
        # assert attr in m.__dict__, msg


def test_if_five_private_attributes_belong_to_instance_storage() -> None:
    """Test that instance dictionary has 5 private attrs
    {'_name': 'Intel-core',
    '_manufacturer': 'Intel',
    '  _total': 0,
    '_allocated': 0,
    '_remaining': 0,
    '_capacity_GB': None}"""
    m = Storage(name="Intel-core", manufacturer="Intel")
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
        assert "_capacity_GB" in m.__dict__



def test_instance_has__6_attributes_storage() -> None:
    m = Storage(name="Intel-core", manufacturer="Intel")
    repr(m)  # need to call installs to create _remaining attr
    attributes = [
        "_name",
        "_manufacturer",
        "_total",
        "_allocated",
        "_remaining",
        "_capacity_GB"
    ]
    for attr in attributes:
        msg = f"The Storage instance does not have {attr} attribute."
        assert hasattr(m, attr), msg


def test_name_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.name, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "name"), property)


def test_manufacturer_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.manufacturer, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "manufacturer"), property)


def test_total_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.total, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "total"), property)


def test_allocated_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.allocated, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "allocated"), property)


def test_remaining_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.remaining, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "remaining"), property)


def test_category_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.category, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "category"), property)


def test_capacity_gb_is_property_storage() -> None:
    with check:
        assert isinstance(Storage.capacity_GB, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Storage, "capacity_GB"), property)

def test_validate_str_is_function_storage() -> None:
    """In child class _validate_str is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage._validate_str,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "_validate_str"),
            types.FunctionType,
        )


def test_validate_int_is_function_storage() -> None:
    """In child class _validate_int is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage._validate_int,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "_validate_int"),
            types.FunctionType,
        )


def test_nt_storage_is_function_storage() -> None:
    with check:
        assert isinstance(
            Storage.__dict__["_nt_storage"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "_nt_storage"),
            types.FunctionType,
        )


def test_nt_resource_is_function_storage() -> None:
    """In child class _nt_resource is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage._nt_resource,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "_nt_resource"),
            types.FunctionType,
        )


def test_purchase_is_function_storage() -> None:
    """In child class purchase is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage.purchase,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "purchase"),
            types.FunctionType,
        )


def test_claim_is_function_storage() -> None:
    """In child class claim is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage.claim,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "claim"),
            types.FunctionType,
        )


def test_freeup_is_function_storage() -> None:
    """In child class freeup is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage.freeup,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "freeup"),
            types.FunctionType,
        )


def test_died_is_function_of_storage() -> None:
    """In child class died is not in class or instance dictionary"""
    with check:
        assert isinstance(
            Storage.died,
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(Storage, "died"),
            types.FunctionType,
        )


def test_purchase_is_callable_storage() -> None:
    assert callable(Storage.purchase), f"'purchase' is not callable."


def test_attributes_name_manufacturer_total_allocated_remaining_are_not_callable_storage() -> (
    None
):
    with check:
        assert not callable(Storage.name), f"'name' is callable."
    with check:
        assert not callable(Storage.manufacturer), f"'manufacturer' is callable."
    with check:
        assert not callable(Storage.total), f"'total' is callable."
    with check:
        assert not callable(Storage.allocated), f"'allocated' is callable."
    with check:
        assert not callable(Storage.remaining), f"'remaining' is callable."
