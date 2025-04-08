import requests
import sqlite3
import os
#import json
def create_table_kinds_makeup(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Makeup_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT VARCHAR(255)
        )
        """)
        cursor.execute("INSERT OR IGNORE INTO Makeup_types (title) VALUES (?)", ("Blush",))
        cursor.execute("INSERT OR IGNORE INTO Makeup_types (title) VALUES (?)", ("Foundation",))
        cursor.execute("INSERT OR IGNORE INTO Makeup_types (title) VALUES (?)", ("Mascara",))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
    
def create_brand_list(fname):
    dir = os.path.dirname(__file__) + os.sep
    fhand = open(os.path.join(dir, fname))
    data = []
    for line in fhand:
       data.append(line.strip()) 
    fhand.close()
    return data
def replace_vow(string, let,brand):
    for val in string:
        brand = brand.replace(val,let)
    return brand


def get_makeup_data(db_file,names):
    data_list = []
    base_url = 'http://makeup-api.herokuapp.com/api/v1/products.json?'
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
    except sqlite3.Error as e:
         print(f"Database error: {e}")
    cur.execute('''SELECT * FROM scraped_data''')
    brand_rank = cur.fetchall()
    for data in brand_rank:
        brand = data[1].lower()
        str_e = "èéêëěẽēėę"
        str_i = "èéêëěẽēėę"
        str_a = "àáâäǎæãåā"
        str_o = "òóôöǒœøõō"
        str_u = "ùúûüǔũūűů"
        brand = replace_vow(str_e,"e",brand)
        brand = replace_vow(str_i,"i",brand)
        brand = replace_vow(str_a,"a",brand)
        brand = replace_vow(str_o,"o",brand)
        brand = replace_vow(str_u,"u",brand)
        for name in names:
            #print(name)
            if name in brand:
                brand = name
                print(brand)
        responce = requests.get(base_url+f"brand={brand}")
        #print(responce.status_code)
        if responce.status_code == 200 and responce.text != []:
            print(responce.url)
            data = responce.text
            print(data)
        #need to loop through the data for each brand to store each blush,mascara,and foundations price
        #for example http://makeup-api.herokuapp.com/api/v1/products.json?brand=covergirl&product_type=foundation

    return data_list

def create_table_makeup(db_file,data_list):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Item_prices (
            product_id INTEGER,
            brand_id TEXT VARCHAR(255),
            price INTEGER
        )
        """)
        cursor.executemany("INSERT INTO Item_prices (title, rank, price) VALUES (?, ?, ?)", data_list)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

db_file = "brand_data.db"
create_table_kinds_makeup(db_file)
data = create_brand_list('brand_list.txt')
data_list = get_makeup_data(db_file,data)
create_table_makeup(db_file,data_list)