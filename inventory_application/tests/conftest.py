# conftest.py
import pytest
from faker import Faker
from inventory_application.apps.resources import Resources
from datetime import datetime, timedelta
from typing import Callable


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


# ---------- for test_resources.py----------------------
@pytest.fixture
def resource_values():
    return {"name": "Parrot", "manufacturer": "Pirates A-Hoy"}


@pytest.fixture
def resource(resource_values):
    return Resources(**resource_values)


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


@pytest.fixture(
    params=[
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
    ]
)
def repr_fixt_cpu(request) -> None:
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def repr_fixt_storage(request) -> None:
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def repr_fixt_hdd(request) -> None:
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def repr_fixt_sdd(request) -> None:
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


@pytest.fixture(
    params=[
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
    ]
)
def str_fixt_cpu(request) -> None:
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def str_fixt_storage(request) -> None:
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def str_fixt_hdd(request) -> None:
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def str_fixt_sdd(request) -> None:
    return request.param


# ------------------for faker, used in test_simple_with_faker ------
@pytest.fixture
def fake():
    fake = Faker()
    fake.seed_instance(1234)
    return fake


# ----------use in any test to truck timing-------------
@pytest.fixture
def time_tracker():
    """In order to use the time tracker in our test we need to mark it as a fixture."""
    start = datetime.now()
    yield  # yield and pass the cpu to run the test
    end = datetime.now()
    diff = end - start
    print(f"\n runtime: {diff.total_seconds()}")
