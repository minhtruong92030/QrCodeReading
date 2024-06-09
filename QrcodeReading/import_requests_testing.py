import requests

def POST(): 
    newData = {
        "name": "PEPSI"
    }
    API = 'http://192.168.0.100/test'
    response = requests.post(API, newData)
    print(response)
    
POST()