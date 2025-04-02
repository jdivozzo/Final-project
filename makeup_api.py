#this was for other idea for now I'll leave it commented out
#API_KEY = 'l4nZwZLVtGkZaAad0mdoxOcqm1cG0dIn'
import requests
base_url = 'http://makeup-api.herokuapp.com/api/v1/products.json?'
brand = "e.l.f."
responce = requests.get(base_url+f"brand={brand}")
if responce.status_code == 200:
    print(responce.text)