import sqlite3
import config


def connection_to_db():
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        create_category_table = """CREATE TABLE IF NOT EXISTS category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL
            );"""
        create_transaction_table = """CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_name TEXT NOT NULL,
                category_id INTEGER,
                amount INTEGER NOT NULL,
                trans_date TEXT NOT NULL,
                FOREIGN KEY (category_id) references category(category_id) ON DELETE CASCADE
            );"""
        create_category_budget_table = """CREATE TABLE IF NOT EXISTS budget (
                category_id INTEGER PRIMARY KEY,
                budget INTEGER NOT NULL,
                FOREIGN KEY (category_id) references category(category_id) ON DELETE CASCADE
        )"""
        cursor.execute(create_category_table)
        cursor.execute(create_transaction_table)
        cursor.execute(create_category_budget_table)
        cursor.close()
    except sqlite3.Error as error:
        print("Error while creating table ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection for DB Connection is closed")
    return

#connection_to_db()