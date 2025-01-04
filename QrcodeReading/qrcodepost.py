import requests

def POST1(valuepost): 
    API = 'http://192.168.224.234/product1'
    response = requests.post(API, valuepost)
    # print(response)

# def POST2(valuepost): 
#     API = 'http://192.168.118.99/product2'
#     response = requests.post(API, valuepost)
    # print(response)

def POST_sysrun(valuepost):
    API = 'http://192.168.224.234/sysrun'
    response = requests.post(API, valuepost)