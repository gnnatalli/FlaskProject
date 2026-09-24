''' Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.

Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.

Задача 3: Определите модель продукта Product со следующими типами колонок:

id: числовой идентификатор

name: строка (макс. 100 символов)

price: числовое значение с фиксированной точностью

in_stock: логическое значение

Задача 4: Определите связанную модель категории Category со следующими типами колонок:

id: числовой идентификатор

name: строка (макс. 100 символов)

description: строка (макс. 255 символов)

Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id. '''


from sqlalchemy import create_engine, String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, relationship, sessionmaker


# Задача 1 - Создаем SQLite базу данных в памяти
engine = create_engine("sqlite:///:memory:", echo=True)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Задача 4 - Модель Category
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(back_populates="category")


# Задача 3 + 5 - Модель продукт
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)


# Задача 5 - связь с Category
    category_id: Mapped[int] = mapped_column(ForeignKey ("categories.id"))

    category: Mapped[Category] = relationship(back_populates="products")


# Создаем таблицы в базе данных
Base.metadata.create_all(engine)


# Задача 2 - создаем фабрику сессий
Session = sessionmaker(bind=engine)

#Создаем сессию
session = Session()
