"""
Модуль для генерации данных для моделей.

Импорты:
    - Импортируются необходимые модули и библиотеки.

Функции:
    - Генерация случайных строк, email, дат, целых чисел.
    - Генерация данных для каждой модели (Application, Users, Modification и т.д.)
"""

import random
import string
from datetime import datetime, timedelta

def random_string(max_length):
    """
    Генерация случайной строки заданной максимальной длины.

    :param max_length: Максимальная длина строки.
    :return: Случайная строка.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(random.randint(1, max_length)))

def random_email(max_length):
    """
    Генерация случайного email с заданной максимальной длиной.

    :param max_length: Максимальная длина email.
    :return: Случайный email.
    """
    domains = ["example.com", "test.com", "mydomain.com"]
    email = f"{random_string(5)}@{random.choice(domains)}"
    return email[:max_length]

def random_date(start, end):
    """
    Генерация случайной даты в заданном диапазоне.

    :param start: Начальная дата диапазона.
    :param end: Конечная дата диапазона.
    :return: Случайная дата.
    """
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_int(min_val, max_val):
    """
    Генерация случайного целого числа в заданном диапазоне.

    :param min_val: Минимальное значение (включительно).
    :param max_val: Максимальное значение (включительно).
    :return: Случайное целое число.
    """
    return random.randint(min_val, max_val)

def generate_application_data(n):
    """
    Генерация списка объектов Application.

    :param n: Количество объектов для генерации.
    :yield: Объект Application.
    """
    from lib.orm import Application
    for _ in range(n):
        yield Application(app_name=random_string(255))

def generate_user_data(n, app_ids):
    """
    Генерация списка объектов Users.

    :param n: Количество объектов для генерации.
    :param app_ids: Список идентификаторов приложений.
    :yield: Объект Users.
    """
    from lib.orm import Users
    now = datetime.now()
    for _ in range(n):
        yield Users(
            full_name=random_string(100),
            email=random_email(255),
            password=random_string(100),
            registration_date=random_date(now - timedelta(days=730), now).date(),
            app_availability=random.choice(app_ids)
        )

def generate_modification_data(n, app_ids):
    """
    Генерация списка объектов Modification.

    :param n: Количество объектов для генерации.
    :param app_ids: Список идентификаторов приложений.
    :yield: Объект Modification.
    """
    from lib.orm import Modification
    for _ in range(n):
        yield Modification(
            mod_name=random_string(100),
            mod_desc=random_string(255),
            app_id=random.choice(app_ids)
        )

def generate_purchase_data(n, user_ids, mod_ids):
    """
    Генерация списка объектов Purchase.

    :param n: Количество объектов для генерации.
    :param user_ids: Список идентификаторов пользователей.
    :param mod_ids: Список идентификаторов модификаций.
    :yield: Объект Purchase.
    """
    from lib.orm import Purchase
    now = datetime.now()
    for _ in range(n):
        yield Purchase(
            user_id=random.choice(user_ids),
            mod_id=random.choice(mod_ids),
            purchase_date=random_date(now - timedelta(days=365), now).date()
        )

def generate_check_data(n, purchase_ids):
    """
    Генерация списка объектов Checks.

    :param n: Количество объектов для генерации.
    :param purchase_ids: Список идентификаторов покупок.
    :yield: Объект Checks.
    """
    from lib.orm import Checks
    for _ in range(n):
        yield Checks(
            purchase_id=random.choice(purchase_ids),
            amount=random.uniform(1, 100),
            payment_method=random_string(50)
        )

def generate_hwid_data(n, user_ids):
    """
    Генерация списка объектов HWID.

    :param n: Количество объектов для генерации.
    :param user_ids: Список идентификаторов пользователей.
    :yield: Объект HWID.
    """
    from lib.orm import HWID
    for _ in range(n):
        yield HWID(
            user_id=random.choice(user_ids),
            processor=random_string(50),
            videocard=random_string(50),
            os_version=random_string(50),
            os_type=random.choice(["32-bit", "64-bit"]),
            disks=random_string(50),
            network_card=random_string(50)
        )

def generate_operation_data(n, user_ids):
    """
    Генерация списка объектов Operation.

    :param n: Количество объектов для генерации.
    :param user_ids: Список идентификаторов пользователей.
    :yield: Объект Operation.
    """
    from lib.orm import Operation
    now = datetime.now()
    for _ in range(n):
        yield Operation(
            user_id=random.choice(user_ids),
            operation_type=random_string(100),
            operation_date=random_date(now - timedelta(days=365), now)
        )

def generate_subscription_data(n, user_ids, mod_ids):
    """
    Генерация списка объектов Subscription.

    :param n: Количество объектов для генерации.
    :param user_ids: Список идентификаторов пользователей.
    :param mod_ids: Список идентификаторов модификаций.
    :yield: Объект Subscription.
    """
    from lib.orm import Subscription
    now = datetime.now()
    for _ in range(n):
        yield Subscription(
            user_id=random.choice(user_ids),
            mod_id=random.choice(mod_ids),
            subscription_time=random_date(now - timedelta(days=365), now)
        )

def generate_token_data(n, user_ids, hwid_ids):
    """
    Генерация списка объектов Token.

    :param n: Количество объектов для генерации.
    :param user_ids: Список идентификаторов пользователей.
    :param hwid_ids: Список идентификаторов HWID.
    :yield: Объект Token.
    """
    from lib.orm import Token
    now = datetime.now()
    for _ in range(n):
        yield Token(
            user_id=random.choice(user_ids),
            hwid_id=random.choice(hwid_ids),
            last_login=random_date(now - timedelta(days=365), now)
        )

def generate_version_data(n, mod_ids):
    """
    Генерация списка объектов Version.

    :param n: Количество объектов для генерации.
    :param mod_ids: Список идентификаторов модификаций.
    :yield: Объект Version.
    """ 
    from lib.orm import Version
    for _ in range(n):
        yield Version(
            mod_id=random.choice(mod_ids),
            version_number=random_int(1, 10),
            version_name=random_string(50),
            version_description=random_string(255),
            version_link=f"http://link{random_string(240)}.com"[:255]  # ограничиваем длину строки до 255 символов
        )