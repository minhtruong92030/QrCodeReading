import requests

def POST(valuepost): 
    API = 'http://192.168.218.99/product'
    response = requests.post(API, valuepost)
    # print(response)

def POST_sysrun(valuepost):
    API = 'http://192.168.218.99/sysrun'
    response = requests.post(API, valuepost)