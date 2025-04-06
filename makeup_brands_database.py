import sqlite3

db_file = "brand_data.db"

def create_table():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT VARCHAR(255),
            rank TEXT
        )
        """)

        conn.commit()
    except sqlite3.Error as e:
         print(f"Database error: {e}")
    finally:
        conn.close()

def insert_data(data_list):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor() 
        cursor.executemany("INSERT INTO scraped_data (title, rank) VALUES (?, ?)", data_list)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()