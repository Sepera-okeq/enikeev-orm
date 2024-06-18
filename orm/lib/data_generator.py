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

def random_string(length):
    """
    Генерация случайной строки заданной длины.

    :param length: Длина строки.
    :return: Случайная строка.
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def random_email():
    """
    Генерация случайного email.

    :return: Случайный email.
    """
    domains = ["example.com", "test.com", "mydomain.com", "economic-crisis.com", "baka.com", "gmail.com", "ya.ru", "mail.ru", "yandex.ru", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com", "tutanota.com", "aol.com", "icloud.com", "inbox.lv", "zoho.com", "gmx.com", "yopmail.com", "mailinator.com", "guerrillamail.com", "10minutemail.com", "temp-mail.org", "maildrop.cc", "dispostable.com", "throwawaymail.com", "tempmailaddress.com", "mailnesia.com", "trashmail.com", "mailsac.com", "getnada.com", "anonaddy.com", "burnermail.io", "simplelogin.io", "scryptmail.com", "mailbox.org", "posteo.de", "tutanota.com", "mailbox.org", "disroot.org", "riseup.net", "autistici.org"]
    email = f"{random_string(5).lower()}@{random.choice(domains)}"
    return email

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

def generate_full_name():
    """
    Генерация случайного ФИО.

    :return: Случайное ФИО.
    """
    first_names = ["Иван", "Темур", "Николай", "Петр", "Алексей", "Дмитрий", "Сергей"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Cпиридонов", "Кукушкин", "Исмагилов"]
    middle_names = ["Алексеевич", "Сергеевич", "Дмитриевич", "Владимирович", "Андреевич"]
    
    return f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(middle_names)}"

def generate_app_name():
    """
    Генерация случайного названия приложения.

    :return: Случайное название приложения.
    """
    app_prefixes = ["Super", "Mega", "Ultra", "Hyper", "Tech"]
    app_suffixes = ["App", "Tool", "Software", "Manager", "System"]
    
    return f"{random.choice(app_prefixes)}{random.choice(app_suffixes)}"

def generate_modification_name():
    """
    Генерация случайного названия модификации.

    :return: Случайное название модификации.
    """
    mod_prefixes = ["Pro", "Lite", "Advanced", "Basic", "Premium", "Free", "Trial", "Ultimate", "Standard", "Professional", "Community"]
    mod_suffixes = ["Edition", "Version", "Setup", "Pack", "Kit", "Release", "Update", "Patch", "Build"]
    
    return f"{random.choice(mod_prefixes)} {random.choice(mod_suffixes)}"

def generate_modification_description():
    """
    Генерация случайного описания модификации.

    :return: Случайное описание модификации.
    """
    descriptions = [
        "Эта модификация включает в себя улучшения производительности",
        "Версия с новыми функциями и исправлениями",
        "Обновление, которое повышает стабильность работы",
        "Новое издание со всеми доступными дополнениями",
        "Более легкая версия с оптимизированными ресурсами",
        "Бесплатная версия для тестирования",
        "Профессиональная версия для опытных пользователей",
        "Сообщество разработчиков представляет новую версию",
        "Версия с расширенными возможностями",
        "Версия для всех пользователей",
        "Сборка с исправлениями уязвимостей и обновлениями",
        "Новое обновление с новыми функциями и улучшениями",
    ]
    
    return random.choice(descriptions)

def generate_payment_method():
    """
    Генерация случайного метода платежа.

    :return: Случайный метод платежа.
    """
    methods = ["Credit Card", "MasterCard", "Visa", "Mir", "Mir Pay", "Tinkoff Pay", "PayPal", "Bank Transfer", "Bitcoin", "Gift Card", "Apple Pay", "Google Pay", "Samsung Pay", "Cash", "Cryptocurrency", "WebMoney", "Yandex Money", "Qiwi Wallet", "Alipay", "WeChat Pay", "Venmo", "Zelle", "Cash App", "Stripe", "Square", "TransferWise", "Revolut", "Payoneer", "Skrill", "Neteller", "Paysera", "Payza", "Perfect Money", "Payeer", "AdvCash", "Paxum", "PaySera", "Epay", "Ecopayz", "WebMoney", "Yandex Money", "Qiwi Wallet", "Alipay", "WeChat Pay", "Venmo", "Zelle", "Cash App", "Stripe", "Square", "TransferWise", "Revolut", "Payoneer", "Skrill", "Neteller", "Paysera", "Payza", "Perfect Money", "Payeer", "AdvCash"]
    
    return random.choice(methods)

def generate_pc_parameters():
    """
    Генерация случайных параметров ПК.

    :return: Словарь с параметрами ПК.
    """
    processors = ["Intel Core i7", "AMD Ryzen 5", "Intel Core i5", "AMD Ryzen 7", "Intel Core i9", "AMD Ryzen 9", "Intel Xeon", "AMD Threadripper", "Intel Pentium", "AMD Athlon", "Intel Celeron", "AMD A-Series"]
    videocards = ["NVIDIA GTX 1650", "AMD Radeon RX 5700", "NVIDIA RTX 2060", "AMD RX 580", "NVIDIA RTX 3080", "AMD RX 6800", "NVIDIA GTX 1050", "AMD RX 560", "NVIDIA RTX 3090", "AMD RX 6900", "NVIDIA GTX 1660", "AMD RX 570", "NVIDIA RTX 3070", "AMD RX 6700", "NVIDIA GTX 1070", "AMD RX 550", "NVIDIA RTX 3060", "AMD RX 6600", "NVIDIA GTX 1080", "AMD RX 5300"]
    os_versions = ["Windows 10", "Windows 11", "Ubuntu 20.04", "macOS Catalina", "Fedora 34", "Debian 11", "CentOS 8", "Arch Linux", "openSUSE Leap", "Linux Mint", "Kali Linux", "Manjaro", "Zorin OS", "Pop!_OS", "elementary OS", "Solus", "Deepin", "MX Linux", "EndeavourOS", "Garuda Linux", "ArcoLinux", "Parrot OS", "Slackware", "Gentoo", "Void Linux", "Alpine Linux", "LFS", "ReactOS", "FreeDOS", "Haiku", "Plan 9", "TempleOS", "RISC OS", "AmigaOS", "BeOS", "QNX", "MS-DOS", "CP/M", "OS/2", "Unix"]
    os_types = ["32-bit", "64-bit"]
    disks = ["HDD 1TB", "SSD 256GB", "Hybrid 1TB", "NVMe SSD 512GB", "SATA SSD 1TB", "M.2 SSD 2TB", "PCIe SSD 1TB", "SAS HDD 2TB", "SCSI HDD 1TB", "eMMC 128GB", "USB Flash 64GB", "SD Card 32GB", "CF Card 16GB", "MicroSD 8GB", "CompactFlash 4GB", "Floppy Disk 1.44MB", "Zip Disk 100MB", "Jaz Disk 1GB", "CD-ROM 700MB", "DVD-RW 4.7GB", "BD-R 25GB", "HD-DVD 15GB", "Blu-ray 50GB", "UHD Blu-ray 100GB", "VHS Tape"]
    network_cards = ["Realtek PCIe", "Intel Ethernet", "Qualcomm Atheros", "Broadcom Ethernet", "Killer Wireless", "Marvell AVASTAR", "Ralink Wireless", "Aquantia AQtion", "ASUS PCE-AC88", "TP-Link Archer", "D-Link DWA", "Netgear Nighthawk", "Linksys WRT", "Cisco Catalyst", "MikroTik Router", "Ubiquiti UniFi", "Zyxel Nebula", "Aruba Instant", "Fortinet FortiGate", "SonicWall TZ", "Palo Alto Networks", "Sophos XG", "Check Point", "Juniper SRX", "F5 BIG-IP", "Citrix NetScaler", "Barracuda CloudGen", "WatchGuard Firebox", "ZyXEL ZyWALL", "Huawei USG", "HPE Aruba", "Ruckus Wireless", "Meraki MR", "Open Mesh", "Mist Systems", "Aerohive HiveAP", "Aruba Instant", "Fortinet FortiAP", "SonicWall SonicPoint", "Palo Alto Networks PA", "Sophos AP", "Check Point 700", "Juniper WLA", "F5 BIG-IP", "Citrix Access Point", "Barracuda CloudGen", "WatchGuard AP", "ZyXEL NWA", "Huawei AP", "HPE Aruba AP", "Ruckus ZoneFlex", "Meraki MR", "Open Mesh AP", "Mist AP", "Aerohive AP"]
    
    return {
        'processor': random.choice(processors),
        'videocard': random.choice(videocards),
        'os_version': random.choice(os_versions),
        'os_type': random.choice(os_types),
        'disks': random.choice(disks),
        'network_card': random.choice(network_cards)
    }

def generate_application_data(n):
    """
    Генерация списка объектов Application.

    :param n: Количество объектов для генерации.
    :yield: Объект Application.
    """
    from lib.orm import Application
    for _ in range(n):
        yield Application(app_name=generate_app_name())

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
            full_name=generate_full_name(),
            email=random_email(),
            password=random_string(12),
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
            mod_name=generate_modification_name(),
            mod_desc=generate_modification_description(),
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
            amount=round(random.uniform(1, 100), 2),
            payment_method=generate_payment_method()
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
        pc_params = generate_pc_parameters()
        yield HWID(
            user_id=random.choice(user_ids),
            processor=pc_params['processor'],
            videocard=pc_params['videocard'],
            os_version=pc_params['os_version'],
            os_type=pc_params['os_type'],
            disks=pc_params['disks'],
            network_card=pc_params['network_card']
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
            operation_type=random_string(15),  # Например, тип операции можно создавать как случайную строку длиной 15
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
    version_prefixes = ["1.0", "1.1", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0", "11.0", "12.0", "13.0", "14.0", "15.0"]
    version_suffixes = ["Alpha", "Beta", "Release", "Stable", "Final"]
    descriptions = [
        "Первоначальный выпуск с базовой функциональностью.",
        "Это обновление включает исправления и улучшения производительности.",
        "Новое крупное обновление с дополнительными функциями.",
        "Исправлены ошибки предыдущих выпусков.",
        "Конечный стабильный выпуск.",
        "Это обновление содержит новые возможности и улучшения.",
        "Сборка с исправлениями уязвимостей и обновлениями.",
        "Новое обновление с новыми функциями и улучшениями.",
        "Это обновление включает исправления и улучшения производительности.",
        "Новое крупное обновление с дополнительными функциями.",
    ]

    for _ in range(n):
        version_number = f"{random.choice(version_prefixes)}.{random_int(0, 9)}"
        version_name = f"{version_number} {random.choice(version_suffixes)}"
        
        yield Version(
            mod_id=random.choice(mod_ids),
            version_number=random_int(1, 200),
            version_name=version_name,
            version_description=random.choice(descriptions),
            version_link=f"http://new-version-{random_string(10)}.com"
        )