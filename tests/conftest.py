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


@pytest.fixture
def parsed_vacancy_dict() -> dict:

    return {
        "hh_id": "128514207",
        "name": "PHP-разработчик",
        "vacancy_link": "https://hh.ru/vacancy/128514207",
        "amount_from": 270000,
        "amount_to": None,
        "currency": "RUB",
        "mode": "За месяц",
        "converted_from": 270000,
        "converted_to": None,
        "required_currency": "RUB",
        "location": "Новосибирск",
        "created_at": "2026-02-01T08:55:32+0300",
        "employer_name": "Токидоки",
        "employer_link": "https://hh.ru/employer/5832652",
        "requirements": "знание современных фреймворков (Symfony или Laravel).",
        "responsibility": "поддержка и доработка сайта компании (японские и корейские автомобильные аукционы).",
    }


@pytest.fixture
def area_codes() -> dict:
    return {
        "россия": {
            "id": 113,
            "regions": {
                "республика марий эл": {
                    "id": 1620,
                    "cities": {
                        "виловатово": 4228,
                        "волжск": 1621,
                        "звенигово": 1622,
                        "знаменский": 4229,
                        "йошкар-ола": 61,
                        "кельмаксола": 4230,
                        "килемары": 4231,
                        "козьмодемьянск": 1623,
                        "красногорский (республика марий эл)": 4232,
                    },
                },
                "москва": {"id": 1, "cities": {}},
                "московская область": {
                    "id": 2019,
                    "cities": {
                        "авсюнино (московская область)": 5976,
                        "автополигон (дмитровский городской округ, московская область)": 144,
                        "александровка (московская область)": 11255,
                        "алпатьево (московская область)": 8190,
                        "алфертищево (московская область)": 11249,
                        "алфимово (московская область)": 8220,
                        "андреевка (московская область)": 6339,
                        "архангельское (московская область)": 8229,
                        "астапово (московская область)": 8181,
                        "ашукино (московская область)": 5968,
                        "балашиха (московская область)": 2020,
                    },
                },
            },
        },
        "беларусь": {
            "id": 16,
            "regions": {
                "брест": {"id": 1007, "cities": {}},
                "брестская область": {
                    "id": 2233,
                    "cities": {
                        "антополь": 11130,
                        "барановичи": 2239,
                        "белоозерск": 2630,
                        "береза": 2240,
                        "большие лепесы": 11861,
                        "большие мотыкалы": 11875,
                        "вишевичи": 11137,
                        "высокое": 2590,
                        "галево": 11135,
                        "ганцевичи": 2241,
                        "давид-городок": 2741,
                        "домачево": 11872,
                    },
                },
            },
        },
        "грузия": {
            "id": 28,
            "regions": {
                "ахалцихе": {"id": 2820, "cities": {}},
                "батуми": {"id": 2814, "cities": {}},
                "болниси": {"id": 2821, "cities": {}},
                "боржоми": {"id": 2822, "cities": {}},
            },
        },
        "другие регионы": {
            "id": 1001,
            "regions": {
                "абхазия": {"id": 2112, "cities": {}},
                "австралия": {"id": 6, "cities": {}},
                "молдова": {
                    "id": 62,
                    "cities": {
                        "бендеры": 11481,
                        "кишинёв": 5049,
                        "комрат": 11482,
                        "тирасполь": 11285,
                        "единец": 11483,
                    },
                },
            },
        },
    }
