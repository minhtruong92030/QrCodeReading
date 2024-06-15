import requests

url = 'http://192.168.124.99/product'

data ={
    'name':'COCA'
}

response = requests.post(url,data)
print(response)