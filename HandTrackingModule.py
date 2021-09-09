import cv2
import mediapipe as mp
import time  


class handDetector():
  def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):  #these prameters are the basic ones

    self.mode=mode
    self.maxHands=maxHands
    self.detectionCon=detectionCon
    self.trackCon=trackCon
    

    
    self.mpHands = mp.solutions.hands 
    self.hands =  self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
    self.mpDraw = mp.solutions.drawing_utils 

    self.tipIds = [4,8,12,16,20] #for the last function


  def findHands(self,img,draw=True):  #draw is used as an flag

    
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    self.results = self.hands.process(imageRGB) 

    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        
        if draw:
          self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS) 
        
    return img #returning the image after drawing on it                             
          

              
  def findPosition(self,img,handNo=0,draw=True):


    self.lmList=[] #an object which will create the position calues


    if self.results.multi_hand_landmarks:
      
       myHand = self.results.multi_hand_landmarks[handNo] #to get the landmark for the particular landmark

       for id,lm in enumerate(myHand.landmark): 
      
        h ,w ,c =img.shape 

        cx , cy = int(lm.x*w ),int(lm.y*h)   

        #print(id,cx,cy)

        self.lmList.append([id,cx,cy])  

        if draw: 
         cv2.circle(img, (cx,cy), 10, (70,80,50), cv2.FILLED) #the landmarks are coloured according to this
       
    return self.lmList #returning the positions of the landmark


  def fingersUp(self):
    
    #this method is added for the hand drawing project
    #the functionality of this method was also used in the hand finger number project 

    ######## also lmlist upr wale function mai define hua hai still we are able to use it in diffrent function   ############
                                        
    fingers = []
  

    #for right hand thumb
    if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]: 
      fingers.append(1)
            
    else:
      fingers.append(0)
        
    #for other fingers
    for id in range(1,5):
    
     if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]: 
      fingers.append(1)
            
     else:
      fingers.append(0)  

    
    return fingers 







def main():

  pTime = 0
  cTime = 0 
  cap = cv2.VideoCapture(0)     
  detector = handDetector() #making an object of our class


  while True:
    
    success , img = cap.read()

    img = detector.findHands(img) #using a function of our class by passing in a parameter ,,,,, img is the processed image after drawing lines on it
    lmList=detector.findPosition(img) #for getting position of the landmark

    if len(lmList) != 0: #to see if it is not empty
      print(lmList[8]) #for now it will print for landmark 8
      

    cTime = time.time()
    fps = 1 / (cTime - pTime) 
    pTime =cTime

    cv2.putText(img,str(int(fps)),(120,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2) 
    cv2.putText(img,"fps is: ",(10,70),cv2.FONT_ITALIC,1,(150,10,10),2)

    cv2.imshow("Image",img) 
    cv2.waitKey(1)








if __name__ == '__main__':
 main() # whatever will be in the main function will showcase what can this module do


