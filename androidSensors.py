import socket, traceback
import xml.etree.ElementTree as ET
import lxml.etree as ET
from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
import cv2
import sys, requests

host = '192.168.43.214'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

# 選擇第二隻攝影機
ip= "192.168.43.1"
port= "6789"
sub_string= "/shot.jpg"
url= "http://"+ ip+ ":"+ port+ sub_string

#used for debugging

print("Success binding")

height, width= 480, 640

# 建立空的畫布
panel = np.zeros((height, width, 3), dtype=np.uint8)

pic= cv2.imread('./pic/sample.png')
pic= cv2.resize(pic, (width, height))

num= 0
while 1:
    num= num+ 1
    
    
    host = '192.168.43.214'
    port = 5555
    if num%15==0:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind((host, port))
        print("ss")

    
    try: 
        img_resp= requests.get(url)
    except:
        print("failue to connect to"+ ip+ "port: "+ port)
        sys.exit(1)
        
    img_arr= np.array(bytearray(img_resp.content), dtype= np.uint8)
    Cam= cv2.imdecode(img_arr, -1)
    Cam= cv2.resize(Cam, (1280, 960))  
    cam= Cam[int(960/4): int(960-(960/4)), int(1280/4): int(1280-(1280/4)), :]    
        
    img= pic.copy()
    message, address = s.recvfrom(8192)
    messageString = message.decode("utf-8")
    
    parser = ET.XMLParser(recover=True)
    tree = ET.ElementTree(ET.fromstring(message, parser=parser)) 
    
    soup = BeautifulSoup(messageString, "html.parser") # accelerometer1
    y= soup.accelerometer1.string
    x= soup.accelerometer2.string

    # Y 軸
    if y[0]=="-":
       y= float(y[1:len(y)])/10*-1
    else:
       y= float(y[0:len(y)])/10
    
    #y= y+ 10
    
    Y=y
    #Y= (20-y)/10
    Y= int(height*0.5)
    
       
       
    # X 軸
    if x[0]=="-":
       x= float(x[1:len(x)])/5*-1
       X= int(width/2+ (x*width/2)*-1)
       img= cv2.circle(img,(X, Y), 10, (0, 255, 255), -1)
    else:
       x= float(x[0:len(x)])/5
       X= int(width/2- (x*width/2)*1)
       img= cv2.circle(img,(X, Y), 10, (0, 255, 255), -1)
    
    sizeWindow= 200
       
    if X- sizeWindow>0 and X+sizeWindow <width:
       if Y- sizeWindow>0 and Y+sizeWindow <height:
          img= cv2.rectangle(img, (X-sizeWindow, Y-sizeWindow), (X+sizeWindow, Y+sizeWindow), (0, 255, 0), 2)
    
    cropImg= pic[int(Y-sizeWindow): int(Y+sizeWindow), int(X-sizeWindow): int(X+sizeWindow), :]
    
    cv2.imshow("img", img)
    
   
    
    

    

    
    try:
        cropImg= cv2.resize(cropImg, (width, height))
        gray= cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
        cropImg[:,:, 0]= np.where(gray>10, cropImg[:,:, 0]*0.4+cam[:,:, 0]*0.6, cam[:,:, 0])
        cropImg[:,:, 1]= np.where(gray>10, cropImg[:,:, 1]*0.4+cam[:,:, 1]*0.6, cam[:,:, 1])
        cropImg[:,:, 2]= np.where(gray>10, cropImg[:,:, 2]*0.4+cam[:,:, 2]*0.6, cam[:,:, 2])
        cv2.imshow("CRP", cropImg)
    except:
        sica= 2
        
    Cam[int(960/4): int(960-(960/4)), int(1280/4): int(1280-(1280/4)), :]=  cropImg[:,:,:]   
    Cam= cv2.resize(Cam, (640, 320))
    cv2.imshow("Cam", Cam)
        
    tempCrop= cropImg
    cropImg
    cv2.waitKey(1)
	
# Example of XML data received:
# <Node Id>node12</Node Id>
# <GPS>
# <Latitude>1.123123</Latitude>
# <Longitude>234.1231231</Longitude>
# <Accuracy>40.0</Accuracy>
# </GPS>
# <Accelerometer>
# <Accelerometer1>0.38444442222</Accelerometer1>
# <Accelerometer2>0.03799999939</Accelerometer2>
# <Accelerometer3>9.19400000331</Accelerometer3>
# </Accelerometer>
# <TimeStamp>1370354489083</TimeStamp>