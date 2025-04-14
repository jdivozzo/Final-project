import sqlite3
import matplotlib.pyplot as plt

def get_plot_data(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
    except sqlite3.Error as e:
         print(f"Database error: {e}")
         
    cur.execute('''SELECT scraped_data.title,scraped_data.rank, Makeup_types.type, Item_prices.price FROM Item_prices JOIN Makeup_types JOIN scraped_data 
                ON Item_prices.product_id = Makeup_types.type_id and Item_prices.brand_id = scraped_data.id''')
    db_data = cur.fetchall()
    conn.close() 
    table_data = {}
    for item in db_data:
        table_data[item[2]] = table_data.get(item[2], [])
        table_data[item[2]].append((item[0].split()[0],item[1],float(item[3])))
    print(table_data['Lipstick'])
    return table_data

def create_visual(table_data):
    # Initialize the plots
    fig = plt.figure(figsize=(10,5))
    ax_b = fig.add_subplot(131)
    ax_e = fig.add_subplot(132)
    ax_f = fig.add_subplot(133)

    #sets up grid
    ax_b.grid()
    ax_e.grid()
    ax_f.grid()

    #sets up titles

    ax_b.set(xlabel='Price', ylabel='Brand Names',
    title='Blush data')

    ax_e.set(xlabel='Price', ylabel='Brand Names',
    title='Eyeliner data')

    ax_f.set(xlabel='Price', ylabel='Brand Names',
    title='Foundation data')

    #get data ready to plot
    by = []
    bx = []
    #blush = sorted(table_data["Blush"], key = lambda t: t[2], reverse = True)
    blush = table_data["Blush"]
    print(blush)
    for val in blush:
        by.append(val[2])
        bx.append(val[0])
    ey = []
    ex = []
    #eyeliner = sorted(table_data["Eyeliner"], key = lambda t: t[2], reverse = True)
    eyeliner = table_data["Eyeliner"]
    print(eyeliner)
    for val in eyeliner:
        ey.append(val[2])
        ex.append(val[0])
    fy = []
    fx = []
    #foundation = sorted(table_data["Foundation"], key = lambda t: t[2], reverse = True)
    foundation = table_data["Foundation"]
    print(foundation)
    for val in foundation:
        fy.append(val[2])
        fx.append(val[0])

    colors = ['grey','blue','orange']
    ax_b.bar(bx,by, color=colors)
    ax_e.bar(ex,ey, color=colors)
    ax_f.bar(fx,fy, color=colors)

    ax_b.set_ylim(0, 25)
    ax_e.set_ylim(0, 25)
    ax_f.set_ylim(0, 25)

    # Show the plot
    plt.tight_layout(pad=1.5)
    fig.savefig("price_for_each_brand.png")
    plt.show()



db_file = "brand_data.db"
table_data = get_plot_data(db_file)
create_visual(table_data)