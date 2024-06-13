import requests

url = 'http://192.168.1.244/test'

data ={
    'name':'TRUONG'
}

response = requests.post(url,data)
print(response)