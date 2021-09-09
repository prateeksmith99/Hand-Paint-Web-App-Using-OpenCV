import cv2
import os 
import HandTrackingModule as htm
import numpy as np
import streamlit as st

st.title("Computer Vision - Camera Hand Paint Web App")
st.text("")
st.markdown('<p>This is a computer vision based project which is using state-of-art computer vision libraries such as MediaPipe which is provided by Google and OpenCV and other libraries such as Streamlit which is providing an interactive UI which works as front-end for the project. </p>', unsafe_allow_html=True)
st.text("")
st.markdown('<p>The following are the ways in which you can use the application :- <p/>',unsafe_allow_html=True)
st.text("")

col1,col2,col3,col4 = st.columns(4)
with col1:
    st.image('1.jpg', width=150)
with col2:
    st.write('Use your Index finger and Middle finger to select a colour')
with col3:
    st.image('2.jpg', width=150)
with col4:
    st.write('Use your Index finger only to draw')


#img1 = Image.open("1.jpg")
#st.image(img1, width=200)

#st.markdown('<h3 style="float: left;">Use your Index finger and Middle finger to select a colour</h3><img style="float: right;" src="2.jpg" />', unsafe_allow_html=True)
#st.markdown('<h3 style="float: left;">Use your Index finger only to draw</h3><img style="float: right;" src="1.jpg" />', unsafe_allow_html=True)

#img2 = Image.open("2.jpg")
#st.image(img2, width=200)

#run = st.checkbox('Run')

st.text("")
st.text("")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(0, 230, 64);
    height: 35px;
    width: 20%;
}
</style>""", unsafe_allow_html=True)

click = st.button('Click to start')
FRAME_WIN = st.image([])

st.text("")
st.text("")
st.text("")
st.text("")
co1,co2 = st.columns(2)
with co1:
    st.markdown('[Source Code ](https://github.com/Aryannath/Hand-Paint-Web-App) ',unsafe_allow_html=True)
with co2:
    st.markdown('[Contact Me ](https://www.linkedin.com/in/prateek-smith-patra-76a3031b5/) ',unsafe_allow_html=True)


while click:

    ###################
    #variables

    overlayList = []
    drawColor =  (0,0,255) #default is red dot
    brushThick = 15 
    xp , yp = 0 , 0
    eraserThick = 80


    ###################

    ###############

    #problem was up because our image keeps updating every iteration so we can not draw on the actual image
    #so we will draw on a new image which is a canvas created using numpy

    imgCanvas = np.zeros((720,1280,3),np.uint8)  

    #there are three channels because we want colured image 
    #by using unit8 which means it will have values from 0-255

    ############### 

    FolderPath = "header"
    myList = os.listdir(FolderPath) #esme sari photos ke naam hai
    #print(myList) for testing


    for imPath in myList:
        image = cv2.imread(f'{FolderPath}/{imPath}') 
        overlayList.append(image) 
    #print(len(overlayList))   for testing
    header = overlayList[0] #for testing the first image


    wCam ,hCam = 1280 , 720 
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)


    
    detector = htm.handDetector(detectionCon=0.85)     

    while True:

        success , img = cap.read()

        
        img = cv2.flip(img,1) #so the right may also apppear right on the screen and the left apper left on the screen
        
        img = detector.findHands(img)
        lmList = detector.findPosition(img,draw=False)

        if len(lmList) != 0:
            #print(lmList)

            x1 = lmList[8][1] #tip of index finger x
            y1 = lmList[8][2] #tip of index finger y
            x2 = lmList[12][1] #tip of middle finger x
            y2 = lmList[12][2] #tip of middle finger y

            #print(x1,y1,x2,y2)


            fingers = detector.fingersUp() #new function made for this project and last project
            #print(fingers)

            if fingers[1] and fingers[2]:  #both index and middle are up

                xp , yp = 0 , 0 # if we don't add it here whenever we are putting two fingers up and then one the new point starts from the point where our one figer was last
                
                #print("selection mode")
                cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,196,0),cv2.FILLED)

                #now we will change the headers

                if y1 < 145: #when the hand is in the header region

                    #x1 values will define the region for selection
                    
                    if 0<x1<240:  #R
                        header = overlayList[0]
                        drawColor = (0,0,255) #here it's BGR not RGB
                        
                        

                    elif 240<x1<520: #G
                        header = overlayList[1]
                        drawColor = (0,255,0)
                        

                    elif 520<x1<780: #B
                        header = overlayList[2]
                        drawColor = (152,25,71)
                        

                    elif 780<x1<1020: #Y
                        header = overlayList[3]
                        drawColor = (0,239,255)
                        

                    elif 1020<x1<1280: #E
                        header = overlayList[4]  
                        drawColor = (0,0,0)
                        

            
            if fingers[1] and fingers[2]==False: #only index is up

                
                
                #print("drawing mode") 
                cv2.circle(img,(x1,y1),20,drawColor,cv2.FILLED)   

                if xp == 0 and yp == 0: #because for the very first frame it will draw the line from (0,0) to that point so we need to change that

                    xp , yp = x1 ,y1

                
                if drawColor == (0,0,0):

                    cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThick)  
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThick)   

                else:

                    cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThick)   #drawing from the old point to the new point
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThick)   #drawing on canvas

                xp , yp = x1 , y1 #updating the points  
        
        #########################################################################
    
        #                           V V IMP

        # first create a gray image then inverted image of it
        # the drawn thing is now black and everything else in the canvas is white in the 'imgInv'
        # then we will merge this inverted on original
        # then we will have black couloured patterns on the original after adding 
        # then we will merge the canvas which has colourd patterns to the original which is currently having black patterns because of the previous merge
        # the colour will overlay the black because of 'OR' operation because things are revere in both rn 
        
        imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY) 
        _ , imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV) 
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,imgInv) #with the and operation the original will get coloured with black from the inverse image
        img = cv2.bitwise_or(img,imgCanvas) #here there is black part on the original and coloured on the canvas this operation will coulor our image
        
        
        ###########################################################################
        
        
        #setting the header image
        h, w, c = header.shape  
        img[0:h , 0:w] = header

        #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0) # this will "BLEND"  both the images not add but this is not very useful so we won't use this

        #cv2.imshow("Image",img) #commented because now we are showing everything in the browser 
        #cv2.imshow("Canvas",imgCanvas) 
        #cv2.imshow("inverse",imgInv) 
        cv2.waitKey(1)


        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        FRAME_WIN.image(img)

        
