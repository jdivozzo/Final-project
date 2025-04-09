# Your name: Jilliann and Cassidy
# Your student id: 
# Your email: jdivozzo@umich.edu and kittycatmckenna@gmail.com
# List who or what you worked with on this homework: N/A
# If you used Generative AI, say that you used it and also how you used it.
# This file will essentially act as our main()

from makeup_brands_scrape import scrape_data
from makeup_brands_database import create_table, insert_data
from visualizations import plot_data, get_data_from_db, clean_data
def main():
    create_table()  # Ensure table exists
    data = scrape_data()  # Scrape data
    insert_data(data)
    
    if len(data) > 0:
        insert_data(data)
        print("Data successfully inserted into the database!")
    else:
        print("No data to insert.")
    raw_data = get_data_from_db()
    cleaned_data = clean_data(raw_data)
    plot_data(cleaned_data)
    

if __name__ == "__main__":
    main()

