import os

from src.excel_manager import ExcelManager
from src.head_hunter_research import HHResearch
from src.salary import Salary
from src.utils import area_code_detector, currency_code_detector


BASE_DIR = os.path.dirname(__file__)


def main() -> None:
    """Функция взаимодействия с пользователем"""

    try:
        manager = ExcelManager()
        saved_vacancies = manager.read_data()
    except PermissionError:
        print(f"Необходимо закрыть файл {BASE_DIR}\\data\\vacancies.xlsx и повторно запустить программу")
    else:
        print(f"Добро пожаловать! Сейчас в базе данных содержится информация о {len(saved_vacancies)} вакансиях.")
        key_words = input("Какую работу вы ищете? ")

        area_yes = input('Введите "ДА", если вы ищете вакансии в каком-то конкретном городе или стране: ')
        area_id = None
        if area_yes.lower() == "да":
            area_id = area_code_detector()

        print("""Для удобства сравнения вакансий по размеру заработной платы все суммы конвертируются в рубли.
Если вам также нужна информация о суммах в другой валюте, введите ее код, например: EUR, USD, CNY, KZT, UZS,
или просто нажмите Enter, если вас устраивает RUB.""")
        user_currency = input()
        user_currency = currency_code_detector(user_currency)
        Salary.set_currency_rates(user_currency)

        hh_object = HHResearch(text=key_words, per_page=100, area=area_id)
        new_vacancies = hh_object.get_response()
        print(f"В интернете для вас найдено дополнительно {len(new_vacancies)} вакансий.")

        manager.update_data(new_vacancies)
        print("Они также сохранены в базе данных.")

        print("""Воспользуйтесь фильтрами, чтобы отобрать наиболее подходящие вакансии:
1 - Не использовать фильтры
2 - Отсортировать вакансии по названию профессии
3 - Отсортировать вакансии по географическому расположению
4 - Отсортировать вакансии по названию организации-работодателя
5 - Отсортировать вакансии по валюте зарплаты""")
        filters_choice = input("Введите комбинацию цифр из предложенных выше вариантов или нажмите Enter: ")
        vacancies = manager.read_data()

        if "1" not in filters_choice:
            if "2" in filters_choice:
                name_keyword = input("Введите название профессии: ")
                vacancies = manager.filter_by_name(name_keyword, vacancies)
            if "3" in filters_choice:
                location_keyword = input("Введите название города: ")
                vacancies = manager.filter_by_location(location_keyword, vacancies)
            if "4" in filters_choice:
                employer_keyword = input("Введите название организации-работодателя: ")
                vacancies = manager.filter_by_employer(employer_keyword, vacancies)
            if "5" in filters_choice:
                currency_keyword = input("Введите код валюты зарплаты, по-умолчанию будет использоваться RUB: ")
                currency_keyword = currency_code_detector(currency_keyword)
                vacancies = manager.filter_by_salary_currency(currency_keyword, vacancies)

        print(f"Отобрано {len(vacancies)} вакансий")
        if len(vacancies) > 0:
            print("""По умолчанию вакансии будут упорядочены от большего к меньшему по величине зарплаты за месяц.
Порядок сортировки можно изменить в соответствии со следующими пунктами:
1 - Выбрать другую периодичность выплат
2 - Принять указанный порядок сортировки от большей зарплаты к меньшей
3 - Сначала показывать вакансии без указанной зарплаты и с наименьшей зарплатой
4 - Сначала показывать самые новые вакансии
5 - Сначала показывать самые старые вакансии""")
            sorters_choice = input("Введите комбинацию цифр из предложенных выше вариантов или нажмите Enter: ")
            mode_choice = "За месяц"
            if "1" in sorters_choice:
                salary_modes = set([vacancy.salary.mode.lower() for vacancy in vacancies if vacancy.salary])
                modes_str = ", ".join(salary_modes)
                mode_choice = input(f"Выберите один из предложенных вариантов порядка выплат:\n{modes_str}:\n")
                if mode_choice.lower() not in salary_modes:
                    mode_choice = "За месяц"
                vacancies = manager.filter_by_salary_mode(mode_choice, vacancies)
            if "2" in sorters_choice:
                if "1" not in sorters_choice:
                    vacancies = manager.filter_by_salary_mode(mode_choice, vacancies)
                vacancies = manager.sort_by_salary(vacancies)
            elif "4" in sorters_choice:
                vacancies = manager.sort_by_date(vacancies)
            elif "5" in sorters_choice:
                vacancies = manager.sort_by_date(vacancies, reverse=True)
            else:
                if "1" not in sorters_choice:
                    vacancies = manager.filter_by_salary_mode(mode_choice, vacancies)
                if "3" in sorters_choice:
                    vacancies = manager.sort_by_salary(vacancies, reverse=True)
                else:
                    vacancies = manager.sort_by_salary(vacancies)
            print_top = input("Введите число вакансий для немедленного ознакомления: ")
            manager.show_top(print_top, vacancies=vacancies)
        print(f"Вся доступная информация о вакансиях сохранена в файл {BASE_DIR}\\data\\vacancies.xlsx")


if __name__ == "__main__":
    main()
