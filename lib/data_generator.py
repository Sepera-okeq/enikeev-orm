import random
import string
from datetime import datetime, timedelta

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def random_email():
    domains = ["example.com", "test.com", "mydomain.com"]
    return f"{random_string(5)}@{random.choice(domains)}"

def random_date(start, end):
    delta = end - start
    int_delta = int(delta.total_seconds())
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def random_int(min_val=1, max_val=10):
    return random.randint(min_val, max_val)

def random_decimals(min_val=1.0, max_val=100.0):
    return round(random.uniform(min_val, max_val), 2)

def generate_applications(n):
    return [{"app_name": f"Company{random_string(5).capitalize()}"} for _ in range(n)]

def generate_users(n, app_ids):
    now = datetime.now()
    return [{
        "full_name": f"{random_string().capitalize()} {random_string().capitalize()}",
        "email": random_email(),
        "password": random_string(16),
        "registration_date": random_date(now - timedelta(days=730), now).date(),
        "app_availability": random.choice(app_ids)
    } for _ in range(n)]

def generate_modifications(n, app_ids):
    return [{
        "mod_name": f"{random_string(8).capitalize()}",
        "mod_desc": f"{random_string(20)}",
        "app_id": random.choice(app_ids)
    } for _ in range(n)]

def generate_purchases(n, user_ids, mod_ids):
    now = datetime.now()
    return [{
        "user_id": random.choice(user_ids),
        "mod_id": random.choice(mod_ids),
        "purchase_date": random_date(now - timedelta(days=365), now).date()
    } for _ in range(n)]

def generate_checks(n, purchase_ids):
    return [{
        "purchase_id": random.choice(purchase_ids),
        "amount": random_decimals(),
        "payment_method": random_string().capitalize()
    } for _ in range(n)]

def generate_hwids(n, user_ids):
    return [{
        "user_id": random.choice(user_ids),
        "processor": f"Processor{random_string(5).capitalize()}",
        "videocard": f"Videocard{random_string(5).capitalize()}",
        "os_version": f"OS{random_string(5).capitalize()}",
        "os_type": random.choice(["32-bit", "64-bit"]),
        "disks": f"{random_string(5).capitalize()}",
        "network_card": f"Network{random_string(5).capitalize()}"
    } for _ in range(n)]

def generate_operations(n, user_ids):
    now = datetime.now()
    return [{
        "user_id": random.choice(user_ids),
        "operation_type": random.choice(["LOGIN", "LOGOUT", "PURCHASE", "UPDATE_PROFILE"]),
        "operation_date": random_date(now - timedelta(days=365), now)
    } for _ in range(n)]

def generate_subscriptions(n, user_ids, mod_ids):
    now = datetime.now()
    return [{
        "user_id": random.choice(user_ids),
        "mod_id": random.choice(mod_ids),
        "subscription_time": random_date(now - timedelta(days=365), now)
    } for _ in range(n)]

def generate_tokens(n, user_ids, hwid_ids):
    now = datetime.now()
    return [{
        "user_id": random.choice(user_ids),
        "hwid_id": random.choice(hwid_ids),
        "last_login": random_date(now - timedelta(days=365), now)
    } for _ in range(n)]

def generate_versions(n, mod_ids):
    return [{
        "mod_id": random.choice(mod_ids),
        "version_number": random_int(1, 10),
        "version_name": f"Version{random_string(5).capitalize()}",
        "version_description": f"Description{random_string(20)}",
        "version_link": f"http://link{random_string(5)}.com"
    } for _ in range(n)]