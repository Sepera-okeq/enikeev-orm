import random
import string
from datetime import datetime, timedelta

# Функции генерации данных
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def random_email():
    domains = ["example.com", "test.com", "economic-crisis.com", "ya.ru"]
    return f"{random_string(5)}@{random.choice(domains)}"

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_int(min_val=1, max_val=10):
    return random.randint(min_val, max_val)

# Генераторы данных для моделей
def generate_application_data(n):
    from lib.orm import Application
    for _ in range(n):
        yield Application(app_name=f"Company{random_string(5).capitalize()}")

def generate_user_data(n, app_ids):
    from lib.orm import Users
    now = datetime.now()
    for _ in range(n):
        yield Users(
            full_name=f"{random_string().capitalize()} {random_string().capitalize()}",
            email=random_email(),
            password=random_string(16),
            registration_date=random_date(now - timedelta(days=730), now).date(),
            app_availability=random.choice(app_ids)
        )

def generate_modification_data(n, app_ids):
    from lib.orm import Modification
    for _ in range(n):
        yield Modification(
            mod_name=f"{random_string(8).capitalize()}",
            mod_desc=f"{random_string(20)}",
            app_id=random.choice(app_ids)
        )

def generate_purchase_data(n, user_ids, mod_ids):
    from lib.orm import Purchase
    now = datetime.now()
    for _ in range(n):
        yield Purchase(
            user_id=random.choice(user_ids),
            mod_id=random.choice(mod_ids),
            purchase_date=random_date(now - timedelta(days=365), now).date()
        )

def generate_check_data(n, purchase_ids):
    from lib.orm import Checks
    for _ in range(n):
        yield Checks(
            purchase_id=random.choice(purchase_ids),
            amount=random.uniform(1, 100),
            payment_method=random_string(10)
        )

def generate_hwid_data(n, user_ids):
    from lib.orm import HWID
    for _ in range(n):
        yield HWID(
            user_id=random.choice(user_ids),
            processor=random_string(10),
            videocard=random_string(10),
            os_version=random_string(5),
            os_type=random.choice(["32-bit", "64-bit"]),
            disks=random_string(5),
            network_card=random_string(5)
        )

def generate_operation_data(n, user_ids):
    from lib.orm import Operation
    now = datetime.now()
    for _ in range(n):
        yield Operation(
            user_id=random.choice(user_ids),
            operation_type=random.choice(["LOGIN", "LOGOUT", "PURCHASE", "UPDATE_PROFILE"]),
            operation_date=random_date(now - timedelta(days=365), now)
        )

def generate_subscription_data(n, user_ids, mod_ids):
    from lib.orm import Subscription
    now = datetime.now()
    for _ in range(n):
        yield Subscription(
            user_id=random.choice(user_ids),
            mod_id=random.choice(mod_ids),
            subscription_time=random_date(now - timedelta(days=365), now)
        )

def generate_token_data(n, user_ids, hwid_ids):
    from lib.orm import Token
    now = datetime.now()
    for _ in range(n):
        yield Token(
            user_id=random.choice(user_ids),
            hwid_id=random.choice(hwid_ids),
            last_login=random_date(now - timedelta(days=365), now)
        )

def generate_version_data(n, mod_ids):
    from lib.orm import Version
    for _ in range(n):
        yield Version(
            mod_id=random.choice(mod_ids),
            version_number=random_int(1, 10),
            version_name=random_string(5).capitalize(),
            version_description=random_string(20),
            version_link=f"http://link{random_string(5)}.com"
        )