
'''

Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных,
обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате JSON.
Задачи:
Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic, 
валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости пользователя.
Написать несколько примеров JSON строк для проверки различных сценариев валидации: 
успешные регистрации и случаи, когда валидация не проходит 
(например возраст не соответствует статусу занятости).

Модели:
Address: Должен содержать следующие поля:
city: строка, минимум 2 символа.
street: строка, минимум 3 символа.
house_number: число, должно быть положительным.

User: Должен содержать следующие поля:
name: строка, должна быть только из букв, минимум 2 символа.
age: число, должно быть между 0 и 120.
email: строка, должна соответствовать формату email.
is_employed: булево значение, статус занятости пользователя.
address: вложенная модель адреса.

Валидация:
Проверка, что если пользователь указывает, что он занят (is_employed = true), 
его возраст должен быть от 18 до 65 лет.

# Пример JSON данных для регистрации пользователя

    json_input = """
{

        "name": "John Doe",

        "age": 70,

        "email": "john.doe@example.com",

        "is_employed": true,

        "address": {

            "city": "New York",

            "street": "5th Avenue",

            "house_number": 123

        }

    } """

'''

import json
from typing import Annotated, reveal_type

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

# Модель адреса
class Address(BaseModel):
    city: Annotated[str, Field(min_length=2, description='City name')]
    street: Annotated[str, Field(min_length=3, description='Street name')]
    house_number: Annotated[int, Field(gt=0, description='Positive house number')]

# Модель пользователя
class User(BaseModel):
    name: Annotated[str, Field(min_length=2, description='User name')]
    age: Annotated[int, Field(gt=0, le=120, description='User age')]
    email: EmailStr
    is_employed: bool
    address: Address


# Проверяем, что имя состоит только из букв
@field_validator("name")
@classmethod
def check_name(cls, value: str):
    if not value.isalpha():
        raise ValueError("Name must be contain only letters")
    return value


# Проверяем соответствие возраста и статуса занятости
@model_validator(mode="after")
def check_employment_age(self):
    if self.is_employed and not 18 <= self.age <= 65:
        raise ValueError("Employment user must be between 18 and 65 years old")
    return self

# Регистрация пользователя
def register_user(json_input: str) -> str:
    try:
        # JSON string -> Pydantic object
        user = User.model_validate_json(json_input)

        # Pydantic object -> JSON string
        return user.model_dump_json()

    except json.JSONDecodeError as e:
        return f"JSON error: {e}"

    except Exception as e:
        return f"Validation error: {e}"


# Успешная регистрация
json_success = """
{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""


# Ошибка: возраст не соответствует статусу занятости
json_age_error = """
{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""


# Ошибка: имя содержит цифры
json_name_error = """
{
    "name": "John Doe123",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""


# Ошибка: неправильный email
json_email_error = """
{
    "name": "John Doe",
    "age": 30,
    "email": "wrong-email",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}
"""


print(register_user(json_success))
print(register_user(json_age_error))
print(register_user(json_name_error))
print(register_user(json_email_error))

