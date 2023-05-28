import pytest
from inventory_application.apps.resources import Resources
from pytest_check import check
import inspect
import types


# --------in case I want to apply the same marker for all below pytest use below. xyz is the name of the marker:-----
# It is a modular fixture. This means that every test function in this file after `pytestmark = pytest.mark.xyz` will
# have this decorator.
# pytestmark = pytest.mark.xyz or pytestmark = [pytest.mark.xyz, pytest.mark.abc]


# to test specific test write: $ pytest -k name_of_the_test

# to check coverage: $ coverage run -m pytest .
# generate coverage report: $ coverage html

# ----------------------- Easy level tests: test Resources with different values ----


@pytest.mark.parametrize(
    "name, manufacturer, expected_name, expected_manufacturer",
    [
        ("Intel-core", "Intel", "Intel-core", "Intel"),
        ("AMD-i9", "AMD", "AMD-i9", "AMD"),
        ("Intel-Pentium", "Intel", "Intel-Pentium", "Intel"),
    ],
)
def test_name_manufacturer(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
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
def test_private_name_manufacture(
    name: str, manufacturer: str, expected_name: str, expected_manufacturer: str
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
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
def test_setter_for_name_manufacturer(
    name: str,
    manufacturer: str,
    new_name: str,
    new_manufacturer: str,
    expected_name: str,
    expected_manufacturer: str,
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
    with check:
        r.name = new_name
        assert r.name == expected_name
    with check:
        r.manufacturer = new_manufacturer
        assert r.manufacturer == expected_manufacturer


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            dict(
                category="resources",
                name="Intel-core",
                manufacturer="Intel",
                total=6,
                allocated=1,
                remaining=5,
            ),
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            dict(
                category="resources",
                name="AMD-i9",
                manufacturer="AMD",
                total=9,
                allocated=0,
                remaining=9,
            ),
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            dict(
                category="resources",
                name="Intel-Pentium",
                manufacturer="Intel",
                total=9,
                allocated=1,
                remaining=8,
            ),
        ),
    ],
)
def test_total_allocated_remaining_category_property(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    expected: dict,
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    with check:
        assert r.total == expected["total"]
    with check:
        assert r.allocated == expected["allocated"]
    with check:
        assert r.remaining == expected["remaining"]
    with check:
        assert r.category == expected["category"]


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            "Resources(category='resources', name='Intel-core', manufacturer='Intel', total=6, allocated=1, remaining=5)",
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            "Resources(category='resources', name='AMD-i9', manufacturer='AMD', total=9, allocated=0, remaining=9)",
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            "Resources(category='resources', name='Intel-Pentium', manufacturer='Intel', total=9, allocated=1, remaining=8)",
        ),
    ],
)
def test_repr_method_v1(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    expected: str,
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    assert repr(r) == expected


def test_repr_method_v2(repr_fixt) -> None:
    name, manufacturer, purchase, claim, freeup, died, expected = repr_fixt
    r = Resources(name=name, manufacturer=manufacturer)
    r.purchase(purchase)
    r.claim(claim)
    r.freeup(freeup)
    r.died(died)
    assert repr(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, expected",
    [
        (
            "Intel-core",
            "Intel",
            "Resources(name='Intel-core', manufacturer='Intel')",
        ),
        (
            "AMD-i9",
            "AMD",
            "Resources(name='AMD-i9', manufacturer='AMD')",
        ),
        (
            "Intel-Pentium",
            "Intel",
            "Resources(name='Intel-Pentium', manufacturer='Intel')",
        ),
    ],
)
def test_str_method_v1(
    name: str,
    manufacturer: str,
    expected: str,
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
    assert str(r) == expected


def test_str_method_v2(str_fixt) -> None:
    name, manufacturer, expected = str_fixt
    r = Resources(name=name, manufacturer=manufacturer)
    assert str(r) == expected


@pytest.mark.parametrize(
    "name, manufacturer, purchase, claim, freeup, died, expected",
    [
        (
            "Intel-core",
            "Intel",
            7,
            3,
            1,
            1,
            "Resources(category='resources', name='Intel-core', manufacturer='Intel', total=6, allocated=1, remaining=5)",
        ),
        (
            "AMD-i9",
            "AMD",
            10,
            4,
            3,
            1,
            "Resources(category='resources', name='AMD-i9', manufacturer='AMD', total=9, allocated=0, remaining=9)",
        ),
        (
            "Intel-Pentium",
            "Intel",
            10,
            7,
            5,
            1,
            "Resources(category='resources', name='Intel-Pentium', manufacturer='Intel', total=9, allocated=1, remaining=8)",
        ),
    ],
)
def test_convert_str_to_instance(
    name: str,
    manufacturer: str,
    purchase: int,
    claim: int,
    freeup: int,
    died: int,
    expected: str,
) -> None:
    r = Resources(name=name, manufacturer=manufacturer)
    rr = eval(str(r))
    rr.purchase(purchase)
    rr.claim(claim)
    rr.freeup(freeup)
    rr.died(died)
    assert repr(rr) == expected


def test_namedtuple_fields() -> None:
    expected_fields = (
        "category",
        "name",
        "manufacturer",
        "total",
        "allocated",
        "remaining",
    )
    r = Resources(name="Intel-core", manufacturer="Intel")
    rr = eval(str(r))
    assert rr._nt_resource()._fields == expected_fields


# ----------------------------- testing how faker package works in testing -----------------------------
def test_name_and_manufacturer_with_faker(fake) -> None:
    d = [
        {"cpu": fake.word().capitalize() + " CPU", "manufacturer": fake.company()}
        for _ in range(100)
    ]
    for dictionary in d:
        r = Resources(dictionary["cpu"], dictionary["manufacturer"])
        with check:
            assert r.name == dictionary["cpu"]
        with check:
            assert r.manufacturer == dictionary["manufacturer"]


# ------------------Test exceptions raised and text of exception correct-----------------------
"""Medium Level Test - test the program runs correctly
given the wrong input information."""


def test_raise_type_exception_should_pass_easy() -> None:
    """test that will catch TypeError exception when it is risen
    and test that the text of the exception is correct"""
    with pytest.raises(TypeError) as e:
        Resources("Intel-core", 1)
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
def test_raise_type_exception_should_pass_parameterize_name(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        Resources(name, manufacturer)
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
def test_raise_type_exception_should_pass_parameterize_manufacturer(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(TypeError) as e:
        Resources(name, manufacturer)
    assert "Unsupported type for value, value must be a string." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [(r, "Intel") for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_name(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        Resources(name, manufacturer)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer",
    [("Intel-core", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_manufacturer(
    name: str, manufacturer: str
) -> None:
    with pytest.raises(ValueError) as e:
        Resources(name, manufacturer)
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
def test_raise_type_exception_should_pass_parameterize_integer(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(TypeError) as e:
        r = Resources(name, manufacturer)
        r.purchase(number)
    assert "Unsupported type for value, value must be a integer." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("Intel-core", "Intel", r) for r in [None, ""]],
)
def test_raise_value_exception_should_pass_parameterize_integer(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Resources(name, manufacturer)
        r.purchase(number)
    assert "value cannot be empty." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer, number",
    [("Intel-core", "Intel", r) for r in [i for i in range(-10, 1)]],
)
def test_raise_value_exception_should_pass_parameterize_integer_is_negative(
    name: str, manufacturer: str, number: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Resources(name, manufacturer)
        r.purchase(number)
    assert "Value must be greater than zero." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim",
    [("Intel-core", "Intel", p, 10) for p in [i for i in range(1, 10)]],
)
def test_raise_value_exception_should_pass_parameterize_claim(
    name: str, manufacturer: str, purchase: int, claim: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Resources(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
    assert "The claimed number cannot be greater than total number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, freeup",
    [("Intel-core", "Intel", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_freeup(
    name: str, manufacturer: str, purchase: int, claim: int, freeup: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Resources(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.freeup(freeup)
    assert "Freeup number cannot be greater than allocated number." == str(e.value)


@pytest.mark.parametrize(
    "name,manufacturer,purchase,claim, died",
    [("Intel-core", "Intel", 20, 10, f) for f in [i for i in range(11, 20)]],
)
def test_raise_value_exception_should_pass_parameterize_died(
    name: str, manufacturer: str, purchase: int, claim: int, died: int
) -> None:
    with pytest.raises(ValueError) as e:
        r = Resources(name, manufacturer)
        r.purchase(purchase)
        r.claim(claim)
        r.died(died)
    assert "The died number is greater than allocated number." == str(e.value)


# ------------- Extra tests -----------------------------
# ----------- test class, function, property types ------
def test_resource_is_instance_of_type() -> None:
    assert isinstance(Resources, type)


# --test that Mod class has 10 attributes --
def test_instance_has_ten_attrs() -> None:
    """Test that class has 10 attrs
    ['allocated',
    'category',
    'claim',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'purchase',
    'remaining',
    'total']"""
    m = Resources(name='Intel-core', manufacturer='Intel')
    actual = len([attr for attr in dir(m) if not attr.startswith("_")])
    expected = 10
    assert actual == expected, f"Mod class does not have {expected} attributes."


def test_instance_has_ten_attributes() -> None:
    """Test that class has 10 attrs
    ['allocated',
    'category',
    'claim',
    'died',
    'freeup',
    'manufacturer',
    'name',
    'purchase',
    'remaining',
    'total']"""
    m = Resources(name='Intel-core', manufacturer='Intel')
    attributes = [attr for attr in dir(m) if not attr.startswith("_")]
    for attr in attributes:
        msg = f"The Mod instance does not have a {attr} attribute."
        assert hasattr(m, attr), msg


def test_if_ten_attributes_belong_to_class() -> None:
    """Test that 10 attrs belongs to class
       ['allocated',
       'category',
       'claim',
       'died',
       'freeup',
       'manufacturer',
       'name',
       'purchase',
       'remaining',
       'total']"""
    m = Resources(name='Intel-core', manufacturer='Intel')
    attributes = [attr for attr in dir(m) if not attr.startswith("_")]
    for attr in attributes:
        msg = f"{attr} attribute is not in instance scope."
        with check:
            assert attr in Resources.__dict__, msg
        with check:
            assert attr in type(m).__dict__, msg
        with check:
            assert attr in m.__class__.__dict__, msg
        # assert attr in m.__dict__, msg


def test_if_five_attributes_belong_to_instance() -> None:
    """Test that instance dictionary has 5 attrs
    {'_name': 'Intel-core',
    '_manufacturer': 'Intel',
    '  _total': 0,
    '_allocated': 0,
    '_remaining': 0}"""
    m = Resources(name='Intel-core', manufacturer='Intel')
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


def test_instance_has__five_attributes() -> None:
    m = Resources(name='Intel-core', manufacturer='Intel')
    repr(m)  # need to call installs to create _remaining attr
    attributes = ["_name", "_manufacturer", "_total", "_allocated", "_remaining"]
    for attr in attributes:
        msg = f"The Resources instance does not have {attr} attribute."
        assert hasattr(m, attr), msg


def test_name_is_property() -> None:
    with check:
        assert isinstance(Resources.name, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Resources, "name"), property)


def test_manufacturer_is_property() -> None:
    with check:
        assert isinstance(Resources.manufacturer, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Resources, "manufacturer"), property)


def test_total_is_property() -> None:
    with check:
        assert isinstance(Resources.total, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Resources, "total"), property)


def test_allocated_is_property() -> None:
    with check:
        assert isinstance(Resources.allocated, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Resources, "allocated"), property)


def test_remaining_is_property() -> None:
    with check:
        assert isinstance(Resources.remaining, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Resources, "remaining"), property)


def test_category_is_property() -> None:
    with check:
        assert isinstance(Resources.category, property)
    # alternatively:
    with check:
        assert isinstance(inspect.getattr_static(Resources, "category"), property)



def test_validate_str_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["_validate_str"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "_validate_str"
            ),
            types.FunctionType,
        )

def test_validate_int_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["_validate_int"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "_validate_int"
            ),
            types.FunctionType,
        )


def test_nt_resource_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["_nt_resource"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "_nt_resource"
            ),
            types.FunctionType,
        )

def test_nt_purchase_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["purchase"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "purchase"
            ),
            types.FunctionType,
        )


def test_claim_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["claim"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "claim"
            ),
            types.FunctionType,
        )


def test_freeup_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["freeup"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "freeup"
            ),
            types.FunctionType,
        )

def test_died_is_function() -> None:
    with check:
        assert isinstance(
            Resources.__dict__["died"],
            types.FunctionType,
        )
    with check:
        assert isinstance(
            inspect.getattr_static(
                Resources, "died"
            ),
            types.FunctionType,
        )


def test_purchase_is_callable() -> (
    None
):
    assert callable(
        Resources.purchase
    ), f"'purchase' is not callable."


def test_attributes_name_manufacturer_total_allocated_remaining_are_not_callable() -> None:
    with check:
        assert not callable(Resources.name), f"'name' is callable."
    with check:
        assert not callable(Resources.manufacturer), f"'manufacturer' is callable."
    with check:
        assert not callable(Resources.total), f"'total' is callable."
    with check:
        assert not callable(Resources.allocated), f"'allocated' is callable."
    with check:
        assert not callable(Resources.remaining), f"'remaining' is callable."