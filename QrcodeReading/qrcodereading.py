import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import urllib.request
import requests

#cap = cv2.VideoCapture(0)

def POST(product): 
    API = 'http://192.168.124.57/test'
    response = requests.post(API, product)
    print('response: ', response)

font = cv2.FONT_HERSHEY_PLAIN

#URL cua Camera IP 
url='http://192.168.124.57'

# Tao cua so de hien thi video truc tiep
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

prev=""
pres=""

a = 0
b = 0

while True:
    img_resp= urllib.request.urlopen(url+'/cam-hi.jpg')
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
 
    #giai ma QRcode tu khung hinh
    decodedObjects = pyzbar.decode(frame)

    for obj in decodedObjects:
        pres=obj.data
        # kiem tra xem QRcode hien tai co khac QRcode truoc do khong
        if prev == pres:
            pass
        else:
            decoded_data = obj.data.decode()
            print("Type:",obj.type)
            print("Data: ",decoded_data)
            
        prev=pres

        #Hien thi du lieu QRcode len khung hinh
        cv2.putText(frame, obj.data.decode(), (70, 70), font, 2,
                    (255, 0, 0), 3)
        
        product = {
            'name': decoded_data
        }      
        if decoded_data == 'COCA' or decoded_data == 'PEPSI':
            POST(product)
        if decoded_data == 'COCA':
            a = a + 1
            print("a = " + str(a))
        if decoded_data == 'PEPSI':
            b = b + 1
            print("b = " + str(b))

    

    #Hien thi khung hinh voi du lieu QRcode
    cv2.imshow("live transmission", frame)
 
    #Kiem tra phim nhan, neu la phim ESC (ma 27) thi thoat khoi vong lap
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()


