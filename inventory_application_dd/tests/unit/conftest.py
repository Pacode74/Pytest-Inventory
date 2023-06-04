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


# ---------- for test_resources.py----------------------


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


# ---------- for test_cpu.py----------------------


@pytest.fixture
def cpu_values():
    return {
        "name": "RYZEN Threadripper 2990WX",
        "manufacturer": "AMD",
        "total": 10,
        "allocated": 3,
        "cores": 32,
        "socket": "sTR4",
        "power_watts": 250,
    }


@pytest.fixture
def cpu(cpu_values):
    return inventory.CPU(**cpu_values)


# ---------- for test_cpu.py----------------------
@pytest.fixture
def storage_values():
    return {
        "name": "Thumbdrive",
        "manufacturer": "Sandisk",
        "total": 10,
        "allocated": 3,
        "capacity_gb": 512,
    }


@pytest.fixture
def storage(storage_values):
    return inventory.Storage(**storage_values)


# ---------- for test_hdd.py----------------------


@pytest.fixture
def hdd_values():
    return {
        "name": "1TB SATA HDD",
        "manufacturer": "Seagate",
        "total": 10,
        "allocated": 3,
        "capacity_gb": 1_000,
        "size": '3.5"',
        "rpm": 10_000,
    }


@pytest.fixture
def hdd(hdd_values):
    return inventory.HDD(**hdd_values)


# ---------- for test_sdd.py----------------------


@pytest.fixture
def ssd_values():
    return {
        "name": "Samsung 860 EVO",
        "manufacturer": "Samsung",
        "total": 10,
        "allocated": 3,
        "capacity_gb": 1_000,
        "interface": "SATA III",
    }


@pytest.fixture
def ssd(ssd_values):
    return inventory.SSD(**ssd_values)
