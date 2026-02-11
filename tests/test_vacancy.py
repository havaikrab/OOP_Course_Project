import pytest

from src.salary import Salary
from src.vacancy import Vacancy


def test_vacancy_init(test_vacancy_dict: dict) -> None:

    some_vacancy = Vacancy(test_vacancy_dict)
    assert some_vacancy._name == "PHP-разработчик"
    assert some_vacancy._vacancy_link == "https://hh.ru/vacancy/128514207"
    assert some_vacancy._location == "Новосибирск"
    assert some_vacancy._created_at == "2026-02-01T08:55:32+0300"
    assert some_vacancy._employer_name == "Токидоки"
    assert some_vacancy._employer_link == "https://hh.ru/employer/5832652"
    assert some_vacancy._requirements == "знание современных фреймворков (Symfony или Laravel)."
    assert (
        some_vacancy._responsibility
        == "поддержка и доработка сайта компании (японские и корейские автомобильные аукционы)."
    )
    assert str(some_vacancy._salary) == " от 270000 RUB за месяц"
    assert str(some_vacancy) == "PHP-разработчик. Зарплата от 270000 RUB за месяц. https://hh.ru/vacancy/128514207"


@pytest.mark.parametrize(
    "vacancy_dict",
    [
        ({"name": "Работник", "alternate_url": "https://hh.ru/vacancy/1"}),
        ({"name": "Вахтер", "alternate_url": "https://hh.ru/vacancy/3", "salary_range": {}}),
        (
            {
                "name": "Директор",
                "alternate_url": "https://hh.ru/vacancy/4",
                "salary_range": {
                    "from": 50000,
                    "to": 60000,
                    "currency": None,
                    "mode": {"id": "MONTH", "name": "За месяц"},
                },
            }
        ),
        (
            {
                "name": "Прораб",
                "alternate_url": "https://hh.ru/vacancy/5",
                "salary_range": {"from": 50000, "to": 60000, "currency": "RUR", "mode": None},
            }
        ),
        (
            {
                "name": "Директор",
                "alternate_url": "https://hh.ru/vacancy/6",
                "salary_range": {"from": 50000, "to": 60000, "currency": "RUR", "mode": {"id": "MONTH", "name": None}},
            }
        ),
    ],
)
def test_vacancy_without_salary(vacancy_dict: dict) -> None:
    some_vacancy = Vacancy(vacancy_dict)
    assert some_vacancy._salary is None
    assert "Зарплата не указана" in str(some_vacancy)


@pytest.mark.parametrize(
    "vacancy_dict",
    [
        ({}),
        (
            {
                "id": "123",
                "name": "Работник",
                "area": {"id": "1", "name": "Россия"},
                "salary_range": {"from": 1000, "currency": "USD"},
            }
        ),
        (
            {
                "id": "123",
                "name": 123,
                "area": {"id": "1", "name": "Россия"},
                "salary_range": {"from": 1000, "currency": "USD"},
                "alternate_url": "https://hh.ru/vacancy/128514207",
            }
        ),
    ],
)
def test_invalid_init(vacancy_dict: dict) -> None:

    with pytest.raises(TypeError):
        Vacancy(vacancy_dict)


def test_validation(test_vacancy_dict: dict, test_other_vacancy_dict: dict) -> None:

    some_vacancy = Vacancy(test_vacancy_dict)
    other_vacancy = str(Vacancy(test_other_vacancy_dict))
    with pytest.raises(TypeError):
        assert some_vacancy == other_vacancy


@pytest.mark.parametrize(
    "self_salary, other_salary",
    [
        (
            {
                "from": 270000,
                "to": 300000,
                "currency": "RUR",
                "gross": False,
                "mode": {"id": "MONTH", "name": "За месяц"},
            },
            {
                "from": 270000,
                "to": 300000,
                "currency": "RUR",
                "gross": False,
                "mode": {"id": "MONTH", "name": "За месяц"},
            },
        ),
        (
            {
                "from": 0,
                "to": 300000,
                "currency": "RUR",
                "gross": False,
                "mode": {"id": "MONTH", "name": "За месяц"},
            },
            {
                "to": 300000,
                "currency": "RUR",
                "gross": False,
                "mode": {"id": "MONTH", "name": "За месяц"},
            },
        ),
        (
            {
                "from": 270000,
                "currency": "RUR",
                "gross": False,
                "mode": {"id": "MONTH", "name": "За месяц"},
            },
            {
                "from": 270000,
                "to": None,
                "currency": "RUR",
                "gross": False,
                "mode": {"id": "MONTH", "name": "За месяц"},
            },
        ),
    ],
)
def test_vacancy_eq(
    self_salary: dict, other_salary: dict, test_vacancy_dict: dict, test_other_vacancy_dict: dict
) -> None:

    some_vacancy = Vacancy(test_vacancy_dict)
    other_vacancy = Vacancy(test_other_vacancy_dict)
    assert some_vacancy == other_vacancy

    some_vacancy._salary = Salary(self_salary)
    other_vacancy._salary = Salary(other_salary)
    assert some_vacancy == other_vacancy


@pytest.mark.parametrize(
    "self_salary_bottom, other_salary_bottom, self_salary_top, other_salary_top",
    [(400000, 200000, 500000, 600000), (0, 300000, 300000, None), (300000, 400000, None, None)],
)
def test_vacancy_lt_le(
    self_salary_bottom: int,
    other_salary_bottom: int,
    self_salary_top: int,
    other_salary_top: int,
    test_vacancy_dict: dict,
    test_other_vacancy_dict: dict,
    test_salary_dict: dict,
) -> None:

    some_vacancy = Vacancy(test_vacancy_dict)
    other_vacancy = Vacancy(test_other_vacancy_dict)
    assert some_vacancy == other_vacancy
    assert some_vacancy <= other_vacancy
    assert some_vacancy >= other_vacancy

    some_salary = Salary(test_salary_dict)
    some_salary.converted_bottom = self_salary_bottom
    some_salary.converted_top = self_salary_top
    some_vacancy._salary = some_salary
    assert some_vacancy > other_vacancy
    assert some_vacancy >= other_vacancy

    other_salary = Salary(test_salary_dict)
    other_salary.converted_bottom = other_salary_bottom
    other_salary.converted_top = other_salary_top
    other_vacancy._salary = other_salary
    assert some_vacancy < other_vacancy
    assert some_vacancy <= other_vacancy

    some_vacancy._salary = None
    assert some_vacancy < other_vacancy
    assert some_vacancy <= other_vacancy

    other_vacancy._salary = None
    assert (some_vacancy < other_vacancy) is False
    assert (some_vacancy <= other_vacancy) is False

    some_vacancy._salary = some_salary
    assert some_vacancy > other_vacancy
    assert some_vacancy >= other_vacancy
