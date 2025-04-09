# Your name: Jilliann and Cassidy
# Your student id: Jilliann – 41643470
# Your email: jdivozzo@umich.edu and kittycatmckenna@gmail.com
# List who or what you worked with on this homework: N/A
# If you used Generative AI, say that you used it and also how you used it.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import json
import re


def scrape_data():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    # setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://wwd.com/lists/top-cosmetic-companies-2023-1236299225/"
    driver.get(url)

    # scroll to load all elements
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # wait for new content to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # stop if no new content is loaded
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()  

    print(soup.prettify()[:2000])  # Print first 2000 characters

    brands = soup.find_all("article", class_="c-gallery-vertical-album") 

    if not brands:
        print("No brand elements found. The class might be incorrect.")

    data_list = []
    for i in range(len(brands)):
        title_tag = brands[i].find("h2", class_="c-gallery-vertical-album__title")
        rank_tag = brands[i].find("span", class_="c-gallery-vertical-album__number")
        sales_tag = brands[i].find("div", class_="c-gallery-vertical-album__description")

        if title_tag and rank_tag and sales_tag:

            title = title_tag.text.strip()
            rank = rank_tag.text.strip()
            sales_text = sales_tag.text.strip()
            match = re.search(r"\$\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s*(?:Billion|Million))?", sales_text)
            sales = match.group(0)
            print("sales: {sales}")

            data_list.append((title, rank, sales))
        else:
            print("Skipping a brand due to missing title or rank or sales.")

    print("Scraped Data:", data_list)
    return data_list

#scrape_data()

def write_data_json_file():
    dir = os.path.dirname(__file__) + os.sep
    out_file = open(os.path.join(dir, 'brand_ranking_data.json'),'w')
    data = scrape_data()
    out_file.write(json.dumps(data, indent=4))
    out_file.close()

write_data_json_file()