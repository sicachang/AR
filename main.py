import cv2
import keyboard

# get sensor data in json formate
import requests
import json

from requests_threads import AsyncSession
session = AsyncSession(n=100)

async def _main():
    # config for ip camera
    ip, port= "192.168.137.83", "5678"
    url = 'http://'+ ip+ ":"+ port+ "/sensors.json"


    width, height= 3000, 1500

    pic= cv2.imread('./sample.png')
    pic= cv2.resize(pic, (width, height))

    y1, x1= 250, 1000
    x= 0
    while (True):
        x= x+ 1
        print(x)
        resp = requests.get(url=url,  verify=False)
        
        data = resp.json() # Check the JSON Response Content documentation below

        img= pic[y1: y1+1000, x1: x1+ 1000, :]
         
        cv2.imshow("img", img)
        cv2.waitKey(1)
        
        print(data["accel"]["data"][0][1][0])
    
        # if keyboard.read_key() == "d":
            # if (x1+5+1000)< width:
                # x1= x1+5
           
        # if keyboard.read_key() == "a":
            # if (x1-5)> 0:
                # x1= x1-5
        #
        
if __name__ == '__main__':
    session.run(_main)        