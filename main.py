import math

import cvzone
import cv2
import numpy
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector=HandDetector(detectionCon=0.8,maxHands=1)

class snakegameclass:
    def __init__(self,pathFood):
        self.points=[]  #all points
        self.lengths=[]  # all lents
        self.currentLength=0
        self.allowedLength= 150  #total allowed length
        self.previousHead=0,0   # privious head points.
        self.imgFood=cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
        self.hfood,self.wfood,_=self.imgFood.shape
        self.foodPoint=0,0
        self.randomFoodLocation()
        self.score=0
        self.gameOver=False

    def randomFoodLocation(self):
        self.foodPoint=numpy.random.randint(100,1000),numpy.random.randint(100,600)

    def update(self,imgMain,currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain,"GAME OVER",[300,400],scale=7,thickness=5,offset=20)
            cvzone.putTextRect(imgMain, f"Score {self.score}", [300, 550], scale=7, thickness=5, offset=20)
        else:
            px,py=self.previousHead
            cx,cy=currentHead

            self.points.append([cx, cy])
            distance=math.hypot(cx-px, cy-py)
            self.lengths.append(distance)
            self.currentLength +=distance
            self.previousHead=cx,cy

            #lenth reduction
            if self.currentLength > self.allowedLength:
                for i,length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.points.pop(i)
                    self.lengths.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
            # check snake eat the food
            rx,ry=self.foodPoint
            if rx-self.wfood//2<cx<rx+self.wfood//2 and  ry-self.hfood//2<cy<ry+self.hfood//2:
                self.randomFoodLocation()
                self.allowedLength+=50
                self.score +=1
                print(self.score)





            #draw snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i!=0:
                        cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            #draw Food
            rx,ry= self.foodPoint
            imgMain=cvzone.overlayPNG(imgMain,self.imgFood,(rx-self.wfood//2,ry-self.hfood//2))

            cvzone.putTextRect(imgMain, f"Score {self.score}", [50, 80], scale=3, thickness=3, offset=10)

            # check for collision
            pts=numpy.array(self.points[:-2],numpy.int32)
            pts= pts.reshape((-1,1,2))
            cv2.polylines(imgMain,[pts],False,(0,200,0),3)
            minDistance=cv2.pointPolygonTest(pts,(cx,cy),True)

            if -1<= minDistance <=1:

                self.gameOver=True
                self.points = []  # all points
                self.lengths = []  # all lents
                self.currentLength = 0
                self.allowedLength = 150  # total allowed length
                self.previousHead = 0, 0  # privious head points.
                self.randomFoodLocation()
                self.score = 0


        return imgMain

game= snakegameclass('C:\\Users\\Ashish\\PycharmProjects\\SnakeGame\\donut.png')


while True:
    success, img=cap.read()
    img=cv2.flip(img,1)
    hands,img= detector.findHands(img,flipType=False)
    if hands:
        lmList=hands[0]['lmList']
        pointIndex=lmList[8][0:2]
        img= game.update(img,pointIndex)



    cv2.imshow("Image", img)
    key= cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver=False


