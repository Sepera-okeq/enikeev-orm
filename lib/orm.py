import re
from enum import Enum

class FieldType(Enum):
    INT = "INT"
    SERIAL = "SERIAL"
    VARCHAR = "VARCHAR"
    DATE = "DATE"
    DATETIME = "TIMESTAMP"
    DECIMAL = "DECIMAL(10,2)"

class OperationType(Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PURCHASE = "PURCHASE"
    UPDATE_PROFILE = "UPDATE_PROFILE"

class Field:
    def __init__(self, type_, primary_key=False, foreign_key=None, max_length=None, min_value=None, max_value=None, many_to_many=False):
        if not isinstance(type_, FieldType):
            raise ValueError("Field type must be an instance of FieldType Enum")
        self.type = type_.value
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value
        self.many_to_many = many_to_many

class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        docstring = dct.get('__doc__')
        if docstring:
            field_definitions = re.findall(
                r'(\w+): FieldType\.(\w+)(, primary_key=True)?(, foreign_key=\'(.+?)\')?(, max_length=(\d+))?(, min_value=(\d+))?(, max_value=(\d+))?(, many_to_many=True)?',
                docstring
            )
            for field_name, field_type, primary_key, _, foreign_key, _, max_length, _, min_value, _, max_value, many_to_many in field_definitions:
                primary_key = bool(primary_key)
                field_type_enum = FieldType[field_type]
                max_length = int(max_length) if max_length else None
                min_value = int(min_value) if min_value else None
                max_value = int(max_value) if max_value else None
                many_to_many = bool(many_to_many)
                dct[field_name] = Field(field_type_enum, primary_key, foreign_key, max_length, min_value, max_value, many_to_many)
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        if not hasattr(cls, '_registry'):
            cls._registry = {}
        else:
            cls._registry[name] = cls
        super(ModelMeta, cls).__init__(name, bases, dct)

class Model(metaclass=ModelMeta):
    primary_keys = {}  # глобальный словарь для хранения первичных ключей каждой таблицы
    many_to_many_tables = []  # глобальный список для хранения таблиц many-to-many

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field) and key not in kwargs:
                setattr(self, key, None)

    @classmethod
    def create_table(cls, db):
        fields = []

        for attr, value in cls.__dict__.items():
            if isinstance(value, Field):
                field_def = f'{attr} {value.type}'
                if value.max_length:
                    field_def = f'{attr} VARCHAR({value.max_length})'
                if value.primary_key:
                    field_def += ' PRIMARY KEY'
                    Model.primary_keys[cls.__name__.lower()] = attr  # сохраняем первичный ключ
                if value.foreign_key:
                    field_def += f' REFERENCES {value.foreign_key}'
                fields.append(field_def)
                if value.many_to_many:
                    Model.many_to_many_tables.append((cls.__name__.lower(), attr, value.foreign_key.split('(')[0], value.foreign_key.split('(')[1][:-1]))

        query = f'CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({", ".join(fields)});'
        with db.get_cursor() as cur:
            cur.execute(query)

    @classmethod
    def create_many_to_many_tables(cls, db):
        for table1, field1, table2, field2 in Model.many_to_many_tables:
            cls.create_many_to_many_table(db, table1, table2, Model.primary_keys)

    @staticmethod
    def create_many_to_many_table(db, table1, table2, primary_keys):
        table_name = f'{table1}_{table2}'
        table1_pk = primary_keys[table1]
        table2_pk = primary_keys[table2]
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table1_pk} INT REFERENCES {table1}({table1_pk}),
            {table2_pk} INT REFERENCES {table2}({table2_pk}),
            PRIMARY KEY ({table1_pk}, {table2_pk})
        );
        '''
        with db.get_cursor() as cur:
            cur.execute(query)

    def extract_field_values(self):
        columns = []
        values = []
        for attr, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                value = getattr(self, attr)
                if isinstance(value, Enum):
                    value = value.value
                if value is None and field.primary_key:
                    continue
                columns.append(attr)
                values.append(value)
        return columns, values

    def save(self, db):
        columns, values = self.extract_field_values()

        if not columns:
            raise ValueError("No fields found to insert.")

        column_names = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        query = f'INSERT INTO {self.__class__.__name__.lower()} ({column_names}) VALUES ({placeholders}) RETURNING *;'
        with db.get_cursor() as cur:
            cur.execute(query, values)
            if self.__class__.__dict__[columns[0]].primary_key:
                setattr(self, columns[0], cur.fetchone()[0])

    @classmethod
    def get_all(cls, db):
        query = f'SELECT * FROM {cls.__name__.lower()};'
        with db.get_cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
            results = []
            for record in records:
                obj = cls(**dict(zip([col[0] for col in cur.description], record)))
                results.append(obj)
            return results

# Пример моделей
class Application(Model):
    """
    app_id: FieldType.SERIAL, primary_key=True
    app_name: FieldType.VARCHAR, max_length=255
    """

class Users(Model):
    """
    user_id: FieldType.SERIAL, primary_key=True
    full_name: FieldType.VARCHAR, max_length=100
    email: FieldType.VARCHAR, max_length=255
    password: FieldType.VARCHAR, max_length=100
    registration_date: FieldType.DATE
    app_availability: FieldType.INT, foreign_key='application(app_id)', min_value=1, max_value=100
    subscriptions: FieldType.INT, foreign_key='modification(mod_id)', many_to_many=True
    """

class Modification(Model):
    """
    mod_id: FieldType.SERIAL, primary_key=True
    mod_name: FieldType.VARCHAR, max_length=100
    mod_desc: FieldType.VARCHAR, max_length=255
    app_id: FieldType.INT, foreign_key='application(app_id)', min_value=1, max_value=100
    """

class Purchase(Model):
    """
    purchase_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)', min_value=1, max_value=100
    mod_id: FieldType.INT, foreign_key='modification(mod_id)', min_value=1, max_value=100
    purchase_date: FieldType.DATE
    """

class Checks(Model):
    """
    check_id: FieldType.SERIAL, primary_key=True
    purchase_id: FieldType.INT, foreign_key='purchase(purchase_id)', min_value=1, max_value=100
    amount: FieldType.DECIMAL
    payment_method: FieldType.VARCHAR, max_length=50
    """

class HWID(Model):
    """
    hwid_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)', min_value=1, max_value=100
    processor: FieldType.VARCHAR, max_length=50
    videocard: FieldType.VARCHAR, max_length=50
    os_version: FieldType.VARCHAR, max_length=50
    os_type: FieldType.VARCHAR, max_length=50
    disks: FieldType.VARCHAR, max_length=50
    network_card: FieldType.VARCHAR, max_length=50
    """

class Operation(Model):
    """
    operation_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)', min_value=1, max_value=100
    operation_type: FieldType.VARCHAR, max_length=100
    operation_date: FieldType.DATETIME
    """

class Subscription(Model):
    """
    subscription_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)', min_value=1, max_value=100
    mod_id: FieldType.INT, foreign_key='modification(mod_id)', min_value=1, max_value=100
    subscription_time: FieldType.DATETIME
    """

class Token(Model):
    """
    token_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)', min_value=1, max_value=100
    hwid_id: FieldType.INT, foreign_key='hwid(hwid_id)', min_value=1, max_value=100
    last_login: FieldType.DATETIME
    """

class Version(Model):
    """
    version_id: FieldType.SERIAL, primary_key=True
    mod_id: FieldType.INT, foreign_key='modification(mod_id)', min_value=1, max_value=100
    version_number: FieldType.INT, min_value=1, max_value=10
    version_name: FieldType.VARCHAR, max_length=50
    version_description: FieldType.VARCHAR, max_length=255
    version_link: FieldType.VARCHAR, max_length=255
    """