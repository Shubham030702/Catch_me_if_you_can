import cv2 as cv
import Pose_estimaton_module as pt
import time
import random
import math

class VideoCamera(object):
    def __init__(self):
        self.video=cv.VideoCapture(0)
        self.video.set(3,1000)
        self.video.set(4,1100)  
        self.ctime = 0
        self.ptime = 0  
        self.game_time = time.time()
        self.start_time = time.time()
        self.position = self.get_random_position()
        self.region = self.position[0]+30 , self.position[1]+30
        self.count = 0
        self.detector = pt.poseDetector()

    def __del__(self):
        self.video.release()

    def get_random_position(self):
        self.x = random.randint(10,1000)
        self.y = random.randint(10,900)
        return self.x,self.y
    
    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv.flip(frame, 1)  # Flip the frame here to correct the mirror image
        frame = self.detector.findPose(frame, draw=False)
        landms = self.detector.findLandmarks(frame, draw=False)
        if len(landms)!=0 :
            x,y=landms[20][1],landms[20][2]
            x1,y1=landms[19][1],landms[19][2]
            distance = math.sqrt((self.position[0] - x) ** 2 + (self.position[1] - y) ** 2)
            distance2 = math.sqrt((self.position[0] - x1) ** 2 + (self.position[1] - y1) ** 2)
            cv.circle(frame,(x,y),20,(255,0,255),-1)
            cv.circle(frame,(x1,y1),20,(255,0,255),-1)
            if (distance<30) | (distance2<30):
                self.count+=1
                self.position = self.get_random_position()    
                region = self.position[0]+30 , self.position[1]+30
                self.start_time = time.time()  
            if time.time() - self.start_time >= 3:
                self.position = self.get_random_position()    
                region = self.position[0]+30 , self.position[1]+30
                self.start_time = time.time()  
        self.ctime = time.time()
        fps = 1/(self.ctime-self.ptime)
        self.ptime = self.ctime
        cv.circle(frame,self.position,20,(255,255,255),-1)
        cv.putText(frame,f'count:-{str(int(self.count))}',(500,70),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,255),3)
        cv.putText(frame,f'FPS:-{str(int(fps))}',(30,70),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,255),3)
        ret, jpeg = cv.imencode('.jpg', frame)
        return jpeg.tobytes()
    
