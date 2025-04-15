# Your name: Jilliann and Cassidy
# Your student id: 
# Your email: jdivozzo@umich.edu and kittycatmckenna@gmail.com
# List who or what you worked with on this homework: N/A
# If you used Generative AI, say that you used it and also how you used it.
# This file will essentially act as our main()

from makeup_brands_scrape import scrape_data
from makeup_brands_database import create_table, insert_data
from makeup_api import create_table_kinds_makeup, create_brand_list, get_makeup_data,create_table_makeup

def main():
    create_table()  # Ensure table exists
    data = scrape_data()  # Scrape data
    insert_data(data)
    
    if len(data) > 0:
        insert_data(data)
        print("Data successfully inserted into the database!")
    else:
        print("No data to insert.")

    db_file = "brand_data.db"
    create_table_kinds_makeup(db_file, ['Blush','Eyeliner','Bronzer','Foundation','Mascara','Eyeshadow','Lipstick','Eyebrow','Lipliner','Nail polish'])
    brand_lst = create_brand_list('brand_list.txt')
    makeup_data = get_makeup_data(db_file,brand_lst)
    if len(makeup_data) > 0:
        create_table_makeup(db_file,makeup_data)
        print("Data successfully inserted into the database!")
    else:
        print("No data to insert.")
    

    from visualizations import plot_data, get_data_from_db, clean_data

    raw_data = get_data_from_db()
    cleaned_data = clean_data(raw_data)
    plot_data(cleaned_data)

    
    

if __name__ == "__main__":
    main()

