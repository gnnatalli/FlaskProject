''' Задача 2: Создание модели для пользователя с настройками
Определите модель UserProfile с полями:
● username (строка),
● password (строка),
● email (строка с валидацией email).
Используйте Field для добавления описаний и настройки валидации пароля
(должен быть не менее 8 символов). '''


from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserProfile(BaseModel):
    username: str = Field(pattern=r"^[a-zA-Z0-9_-]+$", description="Буквыб цифры и '_'")
    password: str = Field(min_length=8, description="Passwort must be at least 8 characters long")
    email: EmailStr


    model_config = ConfigDict(
        json_shema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securePassword123",
                "email": "john.doe@example.com"
            }
        }
    )


# Пример создания пользователя
user_profile = UserProfile(username="john_doe", password="securepassword123", email="john.doe@example.com")
print(user_profile)