import sqlite3
import config


def insert_transaction(trans_data):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        name, category, amount, trans_date = trans_data[0], trans_data[1], trans_data[2], trans_data[3]
        cursor = sqliteConnection.cursor()
        cursor.execute(f"SELECT category_id FROM category WHERE category='{category}'")
        category_id = cursor.fetchall()
        insert_sql = "INSERT INTO transactions (transaction_name, category_id, amount, trans_date) VALUES (?,?,?,?)"

        cursor.execute(insert_sql, (name, int(category_id[0][0]), amount, trans_date))
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for Insert recs is closed")
    #return


def show_transactions():
    try:
        transaction_retrieve_query = ('SELECT t.transaction_name, c.category, t.amount, t.trans_date from '
                                      'transactions t, category c where t.category_id = c.category_id')
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute(transaction_retrieve_query)
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for Show Info closed")


def search_results(text):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT t.transaction_name, c.category, t.amount, t.trans_date from "
                       "transactions t, category c where t.transaction_name LIKE ? AND t.category_id = c.category_id",
                       ('%' + text + '%',))
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for Show Info closed")


def get_category():
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        get_category_query = "SELECT category FROM category"
        cursor.execute(get_category_query)
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Error while getting categories", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for getting categories is closed")


def get_category_id(category_name):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute(f"SELECT category_id FROM category WHERE category='{category_name}'")
        category_id = cursor.fetchall()
        cursor.close()
        return category_id[0][0]
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for Insert recs is closed")


def get_category_transactions(category_name):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        category_id = get_category_id(category_name)
        get_transactions_query = f"SELECT SUM(amount) FROM transactions where category_id = '{category_id}'"
        cursor.execute(get_transactions_query)
        total_amount = cursor.fetchall()
        cursor.close()
        return total_amount[0][0]
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for getting spending per category is closed")


def get_total_expense():
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        get_total_expense_query = f"SELECT SUM(amount) FROM transactions"
        cursor.execute(get_total_expense_query)
        total_expense = cursor.fetchall()
        cursor.close()
        return total_expense[0][0]
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for getting total spent is closed")


def filter_transactions(period):
    try:
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        filter_query = ('SELECT t.transaction_name, c.category, t.amount, t.trans_date from '
                        'transactions t, category c where t.category_id = c.category_id and t.trans_date'
                        ' = CURRENT_DATE')
        if period == "Today":
            filter_query = ('SELECT t.transaction_name, c.category, t.amount, t.trans_date from '
                            'transactions t, category c where t.category_id = c.category_id and'
                            ' t.trans_date = CURRENT_DATE')
        elif period == "Last 7 Days":
            filter_query = ('SELECT t.transaction_name, c.category, t.amount, t.trans_date from '
                            'transactions t, category c where t.category_id = c.category_id and'
                            ' t.trans_date > DATE("now", "-7 days")')
        elif period == "Last 30 Days":
            filter_query = ('SELECT t.transaction_name, c.category, t.amount, t.trans_date from '
                            'transactions t, category c where t.category_id = c.category_id and '
                            't.trans_date > DATE("now", "-30 days")')
        elif period == "All":
            filter_query = ('SELECT t.transaction_name, c.category, t.amount, t.trans_date from '
                            'transactions t, category c where t.category_id = c.category_id')
        cursor.execute(filter_query)
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for getting total spent is closed")

def export_transactions():
    try:
        transaction_retrieve_query = ('SELECT t.transaction_name,c.category, t.amount, t.trans_date from '
                                      'transactions t, category c where t.category_id = c.category_id')
        sqliteConnection = sqlite3.connect(config.DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        cursor.execute(transaction_retrieve_query)
        record = cursor.fetchall()
        desc = cursor.description
        cursor.close()
        return record, desc
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection for Show Info closed")

