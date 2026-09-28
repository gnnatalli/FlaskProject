''' Задача 1: Наполнение данными
Добавьте в базу данных следующие категории и продукты
Добавление категорий: Добавьте в таблицу categories следующие категории:

Название: "Электроника", Описание: "Гаджеты и устройства."
Название: "Книги", Описание: "Печатные книги и электронные книги."
Название: "Одежда", Описание: "Одежда для мужчин и женщин."
Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с
соответствующей категорией:
Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда

Задача 2: Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты,
включая их названия и цены.

Задача 3: Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.

Задача 4: Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.

Задача 5: Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта. '''


from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship



class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(String(100))

    description: Mapped[str] = mapped_column(String(200))

    #  Одна категория = много продуктов
    products: Mapped[list['Product']] = relationship(
        back_populates='category'
    )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(String(100))

    price: Mapped[float] = mapped_column()

    in_stock: Mapped[bool] = mapped_column()

    # Связь с таблицей categories
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id')
    )
    # relationship() позволяет работать с объектом Category
    # через product.category.
    category: Mapped['Category'] = relationship(
        back_populates='products'
    )



engine = create_engine('sqlite:///db.sqlite') # Подключение к SQLite
Base.metadata.create_all(engine) # Создай в базе все таблицы, которые описаны в Base
Session = sessionmaker(bind=engine) # Создает Session для работы с базой данных.

# Задача 1 - наполняем базу данными. Добавляем категории
# with Session() as session:
#
#     electronics = Category(
#         name='Электроника',
#         description='Гаджеты и устройства.'
#     )
#
#     books = Category(
#         name='Книги',
#         description='Печатные книги и электронные книги.'
#     )
#
#     clothes = Category(
#         name='Одежда',
#         description='Одежда для мужчин и женщин.'
#     )
#
# # add_all() добавляет сразу несколько объектов
#     session.add_all([
#         electronics,
#         books,
#         clothes
#     ])
#
# # commit() сохраняет изменения в базе данных.
#     session.commit()


# Проверка - читаем категории из базы
with Session() as session:
# select(Category) — получить записи из таблицы categories.
    query = select(Category)
# scalars() — получаем именно объекты Category.
    categories = session.scalars(query).all()

    for category in categories:
        print(
            category.id,
            category.name,
            category.description
        )

# Задача 1 - добавляем продукты
# with Session() as session:
#     # Сначала получаем категории из базы данных. Находим категорию 'Электроника'
#     electronics = session.scalars(
#         select(Category).where(
#             Category.name == 'Электроника'
#         )
#     ).one()
#
#     # Находим категорию 'Книги'
#     books = session.scalars(
#         select(Category).where(
#             Category.name == 'Книги'
#         )
#     ).one()
#
#     # Находим категорию 'Одежда'
#     clothes = session.scalars(
#         select(Category).where(
#             Category.name == 'Одежда'
#         )
#     ).one()
#
#     # Создаем продукты
#     products = [
#         Product(
#             name='Смартфон',
#             price=299.99,
#             in_stock=True,
#             category=electronics
#         ),
#
#         Product(
#             name='Ноутбук',
#             price=499.99,
#             in_stock=True,
#             category=electronics
#         ),
#
#         Product(
#             name='Научно-фантастический роман',
#             price=15.99,
#             in_stock=True,
#             category=books
#         ),
#
#         Product(
#             name='Джинсы',
#             price=40.50,
#             in_stock=True,
#             category=clothes),
#
#         Product(
#             name='Футболка',
#             price=20.00,
#             in_stock=True,
#             category=clothes
#         )
#     ]
#
#
#     # Добавляем все продукты сразу
#     session.add_all(products)
#
#     # Сохраняем в БД.
#     session.commit()
#
#     print('Продукты добавлены')


# Задача 2 - читаем категории и их продукты
with Session() as session:
    query = select(Category)  # select(Category) - получаем все категории.

    categories = session.scalars(query).all() # scalars() - получаем объекты категории.

    for category in categories:

        print(f'Категория: {category.name}')

        for product in category.products: # category.products - это все продукты, связанные с этой категорией.

            print(f' {product.name} - {product.price}')


# Задача 3 - изменяем цену смартфона

with Session() as session:
    query = select(Product).where(Product.name == 'Смартфон') # Находим продукт с названием "Смартфон"
    # first() возвращает первый найденный объект. Если ничего не найдено → вернёт None.
    smartphone = session.scalars(query).first()

    if smartphone:
        # Меняем цену
        smartphone.price = 349.99

        session.commit() # commit() сохраняет изменение в БД.

        print(
            smartphone.name,
              smartphone.price
        )

# Задача 4 - количество продуктов в каждой категории
with Session() as session:
    query = (
        select(
            Category.name,
            func.count(Product.id)
        )
        .outerjoin(Product) # LEFT JOIN — выводим каждую категорию, даже если продуктов нет
        .group_by(Category.id)
    )

    result = session.execute(query).all()

    for category_name, product_count in result:
        print(
            category_name,
            product_count
        )

# Задача 5 - категории, где больше одного продукта
with Session() as session:
    query = (
        select(
            Category.name,
            func.count(Product.id)
        )
        .join(Product)
        .group_by(Category.id)
        .having(func.count(Product.id) > 1)
    )

    result = session.execute(query).all()

    for category_name, product_count in result:
        print(
            category_name,
            product_count
        )

