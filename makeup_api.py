import requests
import sqlite3
import os
import json
def create_table_kinds_makeup(db_file, lst):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Makeup_types (
            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT VARCHAR(255) UNIQUE)
        """)
        conn.commit()
        for kind in lst:
            cursor.execute("INSERT OR IGNORE INTO Makeup_types (type) VALUES (?)", (kind,))
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

def replace_vow(string, let, brand):
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
    conn.close() 
    #print(brand_rank)
    for data in brand_rank:
        brand = data[1].lower()
        str_e = "èéêëěẽēėę"
        str_i = "ìíîïǐĩīıį"
        str_a = "àáâäǎæãåā"
        str_o = "òóôöǒœøõō"
        str_u = "ùúûüǔũūűů"
        brand = brand.replace("’","'")
        brand = replace_vow(str_e,"e",brand)
        brand = replace_vow(str_i,"i",brand)
        brand = replace_vow(str_a,"a",brand)
        brand = replace_vow(str_o,"o",brand)
        brand = replace_vow(str_u,"u",brand)
        for name in names:
            #print(name)
            if name in brand:
                brand = name
                #print(brand)
        responce = requests.get(base_url+f"brand={brand}")
        #print(responce.status_code)
        if responce.status_code == 200:
            data_j = json.loads(responce.text)
            #print(data)
            if len(data_j) > 0:
                # print(data_j[0])
                # print(data_j[0]["brand"])
                #print(responce.url)
                # print(data_j)
                try:
                    conn = sqlite3.connect(db_file)
                    cur = conn.cursor()
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                    
                cur.execute('''SELECT * FROM Makeup_types''')
                types = cur.fetchall()
                conn.close() 
                for type_info in types:
                    #print(type)
                    type = type_info[1].lower()
                    responce = requests.get(base_url+f"brand={brand}&product_type={type}")
                    if responce.status_code == 200:
                        type_data = json.loads(responce.text)
                        if len(type_data) > 0:
                            t_name = type_data[0]["name"]
                            price = type_data[0]["price"]
                            data_list.append((type_info[0],data[0],t_name,price))
    #print(data_list)

        #need to loop through the data for each brand to store each blush,mascara,and foundations price
        #for example http://makeup-api.herokuapp.com/api/v1/products.json?brand=covergirl&product_type=foundation
    return data_list

def create_table_makeup(db_file,data_list):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Item_prices (
            product_id INTEGER, brand_id TEXT INTEGER,
            product_title TEXT VARCHAR(255) UNIQUE,
            price TEXT
        )
        """)
        cursor.executemany("INSERT OR IGNORE INTO Item_prices (product_id, brand_id,product_title, price) VALUES (?, ?, ?, ?)", data_list)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# db_file = "brand_data.db"
# create_table_kinds_makeup(db_file, ['Blush','Eyeliner','Bronzer','Foundation','Mascara','Eyeshadow','Lipstick','Eyebrow','Lipliner','Nail polish'])
# data = create_brand_list('brand_list.txt')
# data_list = get_makeup_data(db_file,data)
# create_table_makeup(db_file,data_list)