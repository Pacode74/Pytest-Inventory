# conftest.py
import pytest


@pytest.fixture(
    params=[
        (1, 1, 2),
        (2, 2, 4),
        (3, 4, 8),
        (7, 5, 12),
        (12, 6, 18),
    ]
)
def demo_fixt(request):
    # print(f'{request.param=}')
    return request.param
