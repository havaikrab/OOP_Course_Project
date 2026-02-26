from src.utils import detect_inclusions


class MixinFilter:
    """Класс описывающий методы отбора и сортировки вакансий по заданным критериям"""

    @staticmethod
    def filter_by_name(key_word: str, vacancies: list) -> list:
        """Метод отбора вакансий по ключевому слову в названии"""

        return [vacancy for vacancy in vacancies if key_word.lower() in vacancy.name.lower()]

    @staticmethod
    def filter_by_location(key_word: str, vacancies: list) -> list:
        """Метод поиска вакансий в заданной стране, регионе или городе"""

        areas_list = detect_inclusions(key_word.lower())
        if len(areas_list) > 1:
            return [vacancy for vacancy in vacancies if vacancy.location and vacancy.location.lower() in areas_list]
        return [vacancy for vacancy in vacancies if vacancy.location and key_word.lower() in vacancy.location.lower()]

    @staticmethod
    def filter_by_employer(key_word: str, vacancies: list) -> list:
        """Метод отбора вакансий по ключевому слову в названии организации-работодателя"""

        return [
            vacancy
            for vacancy in vacancies
            if vacancy.employer_name and key_word.lower() in vacancy.employer_name.lower()
        ]

    @staticmethod
    def sort_by_date(vacancies: list, reverse: bool = False) -> list:
        """Метод сортировки вакансий по дате создания"""

        return sorted(vacancies, key=lambda vacancy: vacancy.created_at, reverse=not reverse)

    @staticmethod
    def filter_by_salary_mode(mode: str, vacancies: list) -> list:
        """Метод отбора вакансий по режиму выплаты зарплаты"""

        return [vacancy for vacancy in vacancies if not vacancy.salary or vacancy.salary.mode.lower() == mode.lower()]

    @staticmethod
    def filter_by_salary_currency(currency: str, vacancies: list) -> list:
        """Метод отбора вакансий по валюте зарплаты"""

        return [
            vacancy for vacancy in vacancies if vacancy.salary and vacancy.salary.currency.lower() == currency.lower()
        ]

    @staticmethod
    def sort_by_salary(vacancies: list, reverse: bool = False) -> list:
        """Метод сортировки вакансий по величине зарплаты"""

        return sorted(vacancies, reverse=not reverse)

    @staticmethod
    def show_top(top_number: str, vacancies: list) -> None:
        """Метод, выводящий в консоль заданное количество описаний вакансий из переданного списка"""

        top_int = 10
        top_valid = True
        if len(top_number) > 0:
            for i in top_number:
                if not i.isdigit():
                    top_valid = False
                    break
        else:
            top_valid = False
        if top_valid:
            top_int = int(top_number)
        for i in vacancies[:top_int]:
            print(i)
