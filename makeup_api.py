import requests
import json
import os
dir = os.path.dirname(__file__) + os.sep
out_file = open(os.path.join(dir, 'brand_ranking_data.json'))
brand_rank = json.load(out_file)
out_file.close()
base_url = 'http://makeup-api.herokuapp.com/api/v1/products.json?'
brand_data = {}
for data in brand_rank:
    brand = data[0].lower()
    responce = requests.get(base_url+f"brand={brand}")
    if responce.status_code == 200:
        print(responce.url)
        data = responce.text
        print(data)