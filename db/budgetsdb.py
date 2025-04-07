import sqlite3
import config
from db import transactiondb


def get_budget(category_name):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        category_id = transactiondb.get_category_id(category_name)
        get_budget_query = f"SELECT budget FROM budget WHERE category_id = '{category_id}'"
        cursor.execute(get_budget_query)
        record = cursor.fetchall()
        cursor.close()
        return record[0][0]
    except sqlite3.Error as error:
        print("Error while getting budget", error)
        return None
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for Insert recs is closed")


def insert_categories(category):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO category (category) values (?)", (category,))
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while inserting category", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for inserting category is closed")


def insert_budget(category, budget):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        category_id = transactiondb.get_category_id(category)
        insert_budget_query = "INSERT INTO budget (category_id, budget) values (?, ?)"
        cursor.execute(insert_budget_query, (int(category_id), budget))
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while inserting budget", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for inserting budgets is closed")
def total_budgets():
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        get_total_budget_query = f"SELECT SUM(budget) FROM budget"
        cursor.execute(get_total_budget_query)
        total_budget = cursor.fetchall()
        print(total_budget)
        cursor.close()
        return total_budget[0][0]
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for getting total spent is closed")


