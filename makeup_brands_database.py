import sqlite3

db_file = "brand_data.db"

def create_table():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT VARCHAR(255) UNIQUE,
            rank TEXT,
            sales TEXT
        )
        """)

        conn.commit()
    except sqlite3.Error as e:
         print(f"Database error1: {e}")
    finally:
        conn.close()

def insert_data(data_list):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor() 
        new_inserts = 0
        for data in data_list:
            cursor.execute("INSERT OR IGNORE INTO scraped_data (title, rank, sales) VALUES (?, ?, ?)", (data[0], data[1], data[2],))
            if cursor.rowcount == 1:
                new_inserts += 1
            if new_inserts >= 25:
                break
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error2: {e}")
    finally:
        conn.close()