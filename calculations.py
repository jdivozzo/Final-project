
import sqlite3
import os

def get_data(db_data):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
    except sqlite3.Error as e:
         print(f"Database error: {e}")
         
    cur.execute('''SELECT scraped_data.title,scraped_data.sales, Item_prices.price FROM Item_prices JOIN scraped_data 
                ON Item_prices.brand_id = scraped_data.id''')
    db_data = cur.fetchall()
    conn.close() 
    #print(db_data)
    return db_data


def calculate(db_data):
    di = {}
    for data in db_data:
        di[data[0]] = di.get(data[0],[])
        di[data[0]].append((data[1],data[2]))
    di_out = {}
    for k,v in di.items():
        total = 0
        count = 0
        for values in v:
            total += float(values[1])
            count += 1
        di_out[k] = (v[0][0],total/count)
    return di_out

def write_txt(di):
    dir = os.path.dirname(__file__) + os.sep
    out_file = open(os.path.join(dir, 'calculations.txt'),'w')
    for k,v in di.items():
        out_file.write(f"Name: {k} Sales: {v[0]} Average Price per product: {v[1]}\n\n")
    out_file.close()

