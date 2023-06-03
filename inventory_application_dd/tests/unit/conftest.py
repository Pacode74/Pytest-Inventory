# conftest.py
import pytest
from faker import Faker
from inventory_application_dd.apps.models import inventory


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


# ------------------for faker, used in test_simple_with_faker ------
@pytest.fixture
def fake():
    fake = Faker()
    fake.seed_instance(1234)
    return fake


# ---------- for test_create_resource_use_fixture----------------------


@pytest.fixture
def resource_values():
    return {
        "name": "Parrot",
        "manufacturer": "Pirates A-Hoy",
        "total": 100,
        "allocated": 50,
    }


@pytest.fixture
def resource(resource_values):
    return inventory.Resource(**resource_values)
