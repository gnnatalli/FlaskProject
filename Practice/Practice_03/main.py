from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models import User, Address, Base

engine = create_engine('sqlite:///practicum3.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:

     #  1. Напишите запрос, который возвращает пользователя с конкретным именем(например, "Alice").
    query = select(User).where(User.name == 'Alice')
    user = session.scalars(query).first()

    print(f"User: {user.id}, name: {user.name}, age: {user.age}")

# 2. Напишите запрос для вывода всех пользователей, возраст которых больше 20 лет.
    query = select(User).where(User.age > 20)
    users = session.execute(query).scalars().all()
    print("Users older than 20")
    for user in users:
         print(f"User: {user.id}, name: {user.name}, age: {user.age}")


# 3. Допустим, вы хотите обновить возраст пользователя "Bob" до 25 лет. Напишите
# запрос для обновления данных.
    query = select(User).where(User.name == "Bob")
    user_to_update = session.scalar(query)
    if user_to_update:
         user_to_update.age = 20
         session.add(user_to_update)
         session.commit()
         print(f"Updated Bob's age to {user_to_update.age}")

# 4. Напишите запрос для вывода всех пользователей, возраст которых меньше 30 лет.
# Выведите их имена и возраст.
    query = select(User).where(User.age < 30)
    users = session.execute(query).scalars().all()

    print("Users older than 30:")

    for user in users:
        print(f"User: {user.id}, name: {user.name}, age: {user.age}")

# 5. Напишите запрос, который добавляет пользователя с именем "Charlie".
    new_user = User(name="Charlie", age=22)

    session.add(new_user)
    session.commit()

    print(f"User added: {new_user.id}, name: {new_user.name}, age: {new_user.age}")

# 6. Напишите запрос, который удаляет пользователя с определённым именем "Charlie".
# Выведите информацию о том, был ли он удален.
    query = select(User).where(User.name == "Charlie")
    user = session.scalars(query).first()

    if user:
        session.delete(user)
        session.commit()
        print(f"User {user.name} was deleted.")
    else:
        print("User Charlie was not found.")

# 7. Создайте запрос, который выводит всех пользователей, отсортированных по
# возрасту в порядке убывания.
    query = select(User).order_by(User.age.desc())
    users = session.scalars(query).all()

    print("Users sorted by age (descending):")

    for user in users:
        print(f"User: {user.id}, name: {user.name}, age: {user.age}")

# 8. Напишите запрос, который выводит первые 4 пользователя, отсортированных по
# имени в алфавитном порядке.
    query = select(User).order_by(User.name).limit(4)
    users = session.scalars(query).all()

    print("First 4 users alphabetically:")

    for user in users:
        print(f"User: {user.id}, name: {user.name}, age: {user.age}")

# 9. Напишите запрос для обновления данных пользователя, используя его id.
# Предположим, нужно обновить возраст пользователя с id равным 5 до 35 лет.
    query = select(User).where(User.id == 5)
    user = session.scalars(query).first()

    if user:
        user.age = 35
        session.commit()
        print(f"User {user.id} updated. New age: {user.age}")
    else:
        print(f"User with id 5 was not found.")

# 10. Напишите запрос, который проверяет, существует ли пользователь с заданным name.
# Проверьте наличие пользователя с name равным "Charlie".
    query = select(User).where(User.name == "Charlie")
    user = session.scalars(query).first()

    if user:
        print("User with name Charlie exists.")
    else:
        print("User Charlie does not exist.")

# 11. Напишите запрос, который находит средний возраст всех пользователей, и выведите
# результат.
    query = select(func.avg(User.age))
    average_age = session.scalar(query)

    print(f"Average age: {average_age:.2f}")

# 12. Создайте запрос, который найдет максимальный и минимальный возраст среди
# пользователей. Используйте функции func.max() и func.min().
    query = select(
        func.max(User.age),
        func.min(User.age)
    )

    max_age, min_age = session.execute(query).one()

    print(f"Max age: {max_age}")
    print(f"Min age: {min_age}")



