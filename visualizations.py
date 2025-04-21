import sqlite3
import matplotlib.pyplot as plt
import re

db_file = "brand_data.db"

def get_data_from_db():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT title, rank, sales FROM scraped_data")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Database error: {e}")
        return []
    finally:
        conn.close()


def parse_sale(sales):
    sales_pattern = r"\$([\d\.]+)\s*(Billion|Million)?"
    match = re.search(sales_pattern, sales)
    if match:
        number = float(match.group(1))
        unit = match.group(2)
        if unit:
            if unit in ["Million"]:
                number /= 1000  # put into billions
            elif unit in ["Billion"]:
                pass  # if already in billions
        return number
    return None

def clean_data(data):
    cleaned = []
    for title, rank, sale in data:
        try:
            rank_num = int(''.join(filter(str.isdigit, rank)))
            sale_val = parse_sale(sale)
            if sale_val is not None:
                cleaned.append((title, rank_num, sale_val))
        except ValueError:
            continue
    return cleaned


def plot_top_data(data_list):
    if not data_list:
        print("No data to plot")
        return

    data_list = sorted(data_list, key=lambda x: x[1])[:10]  # confirm sorted by rank
    titles = [item[0] for item in data_list]
    sales = [item[2] for item in data_list]
    plt.rcParams.update({'font.size': 10}) # Set font size to 14
    fig = plt.figure(figsize=(12, 8))
    plt.barh(titles, sales, color='blue')
    plt.xlabel('Sales (in billions)')
    plt.title('Top Makeup Brand Sales by Rank')
    plt.gca().invert_yaxis()  # highest rank at the top
    plt.tight_layout()
    fig.savefig("Top_brands_by_rank")
    plt.show()

def plot_bottom_data(data_list):
    if not data_list:
        print("No data to plot")
        return

    bottom_data = data_list[-10:]
    titles = [item[0] for item in bottom_data]
    sales = [item[2] for item in bottom_data]
    plt.rcParams.update({'font.size': 10}) # Set font size to 14
    fig = plt.figure(figsize=(12, 8))
    plt.barh(titles, sales, color='blue')
    plt.xlabel('Sales (in billions)')
    plt.title('Bottom Makeup Brand Sales by Rank')
    plt.gca().invert_yaxis()  # highest rank at the top
    plt.tight_layout()
    fig.savefig("Bottom_brands_by_rank")
    plt.show()


            

