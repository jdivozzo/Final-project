
import sqlite3
import os

def get_data(db_data,db_file):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
    except sqlite3.Error as e:
         print(f"Database error: {e}")
         
    cur.execute('''SELECT scraped_data.title,scraped_data.sales, Item_prices.price, Makeup_types.type FROM Item_prices JOIN Makeup_types JOIN scraped_data 
                ON Item_prices.product_id = Makeup_types.type_id and Item_prices.brand_id = scraped_data.id''')
    db_data = cur.fetchall()
    conn.close() 
    #print(db_data)
    return db_data


def calculate(db_data):
    di = {}
    for data in db_data:
        di[data[0]] = di.get(data[0],[])
        di[data[0]].append((data[1],data[2],data[3]))
    #print(di)
    di_out = {}
    for k,v in di.items():
        total = 0
        count = 0
        type_m = {}
        for values in v:
            total += float(values[1])
            type_m[values[2]] = di_out.get(values[2], 0) + 1
            count += 1
        di_out[k] = (v[0][0],total/count,type_m)
    #print(di_out)
    return di_out

def write_txt(di):
    dir = os.path.dirname(__file__) + os.sep
    out_file = open(os.path.join(dir, 'calculations.txt'),'w')
    for k,v in di.items():
        blush = v[2].get("Blush", 0)
        eyeliner = v[2].get("Eyeliner", 0)
        bronzer = v[2].get("Bronzer", 0)
        foundation = v[2].get("Foundation", 0)
        mascara = v[2].get("Mascara", 0)
        eyeshadow = v[2].get("Eyeshadow", 0)
        lipstick = v[2].get("Lipstick", 0)
        nail_polish = v[2].get("Nail polish", 0)
        out_file.write(f"Name: {k} Sales: {v[0]} Average Price per product: {v[1]}\nAverage Price calculated from: {blush} Blush, {eyeliner} Eyeliner, {bronzer} Bronzer, {foundation} Foundation, {mascara} Mascara, {eyeshadow} Eyeshadow, {lipstick} Lipstick, {nail_polish} Nail polish\n\n")
    out_file.close()

# db_file = "brand_data.db"
# db_data = get_data(db_file,db_file)
# di = calculate(db_data)
# write_txt(di)