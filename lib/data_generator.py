import random
import string
from datetime import datetime, timedelta

# Функции генерации данных
def random_string(max_length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(random.randint(1, max_length)))

def random_email(max_length):
    domains = ["example.com", "test.com", "mydomain.com"]
    email = f"{random_string(5)}@{random.choice(domains)}"
    return email[:max_length]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_int(min_val, max_val):
    return random.randint(min_val, max_val)

# Генераторы данных для моделей
def generate_application_data(n):
    from lib.orm import Application
    for _ in range(n):
        yield Application(app_name=random_string(255))

def generate_user_data(n, app_ids):
    from lib.orm import Users
    now = datetime.now()
    for _ in range(n):
        yield Users(
            full_name=random_string(100),
            email=random_email(255),
            password=random_string(100),
            registration_date=random_date(now - timedelta(days=730), now).date(),
            app_availability=random_int(1, 100)
        )

def generate_modification_data(n, app_ids):
    from lib.orm import Modification
    for _ in range(n):
        yield Modification(
            mod_name=random_string(100),
            mod_desc=random_string(255),
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
            payment_method=random_string(50)
        )

def generate_hwid_data(n, user_ids):
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
    from lib.orm import Operation
    now = datetime.now()
    for _ in range(n):
        yield Operation(
            user_id=random.choice(user_ids),
            operation_type=random_string(100),
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
            version_name=random_string(50),
            version_description=random_string(255),
            version_link=f"http://link{random_string(255)}.com"
        )