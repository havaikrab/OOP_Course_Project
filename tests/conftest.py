import pytest


@pytest.fixture
def test_salary_dict() -> dict:
    return {
        "from": 270000,
        "to": 300000,
        "currency": "RUR",
        "gross": False,
        "mode": {"id": "MONTH", "name": "За месяц"},
    }
