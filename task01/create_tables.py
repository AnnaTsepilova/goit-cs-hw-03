import psycopg2
from dotenv import dotenv_values

# Завантажуємо змінні середовища з .env файлу
config = dotenv_values('.env')

# Задаємо параметри для заповнення таблиць

database_config = {
    'dbname': config['DBNAME'],
    'user': config['USER'],
    'password': config['PASSWORD'],
    'host': config['HOST']
}


# Функція для підключеня до бази даних і створення таблиць
def create_table(create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    conn = None
    try:
        conn = psycopg2.connect(**database_config)
        print("З базою даних успішно з'єднано!")
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        print("Таблиці успішно створені!")

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(f"Сталася помилка: {error}")

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    # Задаємо параметри для створення таблиць
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """

    create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
     id SERIAL PRIMARY KEY,
     title VARCHAR(100) NOT NULL,
     description TEXT,
     status_id INTEGER,
     user_id INTEGER,
     FOREIGN KEY (status_id) REFERENCES status (id),
     FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """
    # Створюємо таблицю users
    create_table(create_users_table)
    # Створюємо таблицю status
    create_table(create_status_table)
    # Створюємо таблицю tasks
    create_table(create_tasks_table)
