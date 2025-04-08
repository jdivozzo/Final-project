import sqlite3
import matplotlib.pyplot as plt

db_file = "brand_data.db"

def get_data_from_db():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT title, rank FROM scraped_data")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Database error: {e}")
        return []
    finally:
        conn.close()

def plot_data(data_list):
    
