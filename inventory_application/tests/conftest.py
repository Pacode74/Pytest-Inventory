# conftest.py
import pytest
from faker import Faker


# --------------------- used for basic test to check that CI works correctly------------------
@pytest.fixture(
    params=[
        (1, 1, 2),
        (2, 2, 4),
        (3, 4, 7),
        (7, 5, 12),
        (12, 6, 18),
    ]
)
def demo_fixt(request):
    """fixture for basic test to test basic app"""
    # print(f'{request.param=}')
    return request.param


# ------------------used in test_repr_method_v2 ----------------------


@pytest.fixture(
    params=[
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
    ]
)
def repr_fixt(request) -> None:
    return request.param


# ------------------used in test_str_method_v2 ----------------------


@pytest.fixture(
    params=[
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
    ]
)
def str_fixt(request) -> None:
    return request.param


# ------------------for faker, used in test_simple_with_faker ------
@pytest.fixture
def fake():
    fake = Faker()
    fake.seed_instance(1234)
    return fake
