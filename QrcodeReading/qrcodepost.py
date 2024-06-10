import requests

def POST(valuepost): 
    API = 'http://192.168.124.57/test'
    response = requests.post(API, valuepost)
    print(response)
