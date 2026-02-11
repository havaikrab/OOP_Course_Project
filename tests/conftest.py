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


@pytest.fixture
def test_vacancy_dict() -> dict:
    return {
        "id": "128514207",
        "name": "PHP-разработчик",
        "area": {"id": "4", "name": "Новосибирск", "url": "https://api.hh.ru/areas/4"},
        "salary": {"from": 270000, "to": None, "currency": "RUR", "gross": False},
        "salary_range": {
            "from": 270000,
            "to": None,
            "currency": "RUR",
            "gross": False,
            "mode": {"id": "MONTH", "name": "За месяц"},
            "frequency": {"id": "TWICE_PER_MONTH", "name": "Два раза в месяц"},
        },
        "type": {"id": "open", "name": "Открытая"},
        "address": {
            "city": "Новосибирск",
            "street": "Советская улица",
            "building": "64",
            "lat": 55.048513,
            "lng": 82.911482,
            "raw": "Новосибирск, Советская улица, 64",
            "metro": {
                "station_name": "Гагаринская",
                "line_name": "Ленинская",
                "station_id": "52.295",
                "line_id": "52",
                "lat": 55.051071,
                "lng": 82.91477,
            },
            "metro_stations": [
                {
                    "station_name": "Гагаринская",
                    "line_name": "Ленинская",
                    "station_id": "52.295",
                    "line_id": "52",
                    "lat": 55.051071,
                    "lng": 82.91477,
                }
            ],
            "id": "6742717",
        },
        "published_at": "2026-02-01T08:55:32+0300",
        "created_at": "2026-02-01T08:55:32+0300",
        "url": "https://api.hh.ru/vacancies/128514207?host=hh.ru",
        "alternate_url": "https://hh.ru/vacancy/128514207",
        "relations": [],
        "employer": {
            "id": "5832652",
            "name": "Токидоки",
            "url": "https://api.hh.ru/employers/5832652",
            "alternate_url": "https://hh.ru/employer/5832652",
            "logo_urls": {
                "original": "https://img.hhcdn.ru/employer-logo-original-round/6341088.png",
                "90": "https://img.hhcdn.ru/employer-logo-round/6341090.png",
                "240": "https://img.hhcdn.ru/employer-logo-round/6341091.png",
            },
            "vacancies_url": "https://api.hh.ru/vacancies?employer_id=5832652",
            "country_id": 1,
        },
        "snippet": {
            "requirement": "знание современных фреймворков (Symfony или Laravel).",
            "responsibility": "поддержка и доработка сайта компании (японские и корейские автомобильные аукционы).",
        },
        "contacts": None,
        "schedule": {"id": "remote", "name": "Удаленная работа"},
        "professional_roles": [{"id": "96", "name": "Программист, разработчик"}],
    }


@pytest.fixture
def test_other_vacancy_dict() -> dict:
    return {
        "id": "3333",
        "name": "Работник",
        "area": {"id": "1", "name": "Россия"},
        "salary": {"from": 270000, "currency": "RUR", "gross": False},
        "created_at": None,
        "employer": {},
        "alternate_url": "https://hh.ru/vacancy/128514207",
        "salary_range": {
            "from": 270000,
            "currency": "RUR",
            "mode": {"name": "За месяц"},
        },
    }
