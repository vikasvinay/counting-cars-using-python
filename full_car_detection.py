import numpy as np
import os ,sys
import cv2
import time
from PIL import Image
import RPi.GPIO as GPIO

filename = 'cars.avi'
frames_per_second = 24.0
res = '480p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720), #using this size
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


capture_duration = 20  # time to rec 20sec(21sec) = 283img
cap = cv2.VideoCapture(1)
out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

start_time = time.time()  #time function
while int(time.time() - start_time) < capture_duration:  #imp condetion to work
    ret, frame = cap.read()
    out.write(frame)
    if ret==True:
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

#///////////////////////////////////////////////////////////////////////////////

#//////////////////////////////////////video converter

vidcap = cv2.VideoCapture('cars.avi')
success, image = vidcap.read()
count = 0
success = True
while success:
  cv2.imwrite("New folder/%d.jpg" % count, image)     # save frame as JPEG file
  success,image = vidcap.read()
  print ('Read a new frame: ', success)
  count += 1

#///////////////////////resize img
#path = "New folder/"
#dirs = os.listdir( path )

#def resize():
#    for item in dirs:
 #       if os.path.isfile(path+item):
  #          im = Image.open(path+item)
   #         f, e = os.path.splitext(path+item)
    #        imResize = im.resize((1288,1480), Image.ANTIALIAS)
     #       imResize.save(f + '.jpg', 'JPEG', quality=90)

#resize()



#/////////////////////////////////////////////////image slicer

# load the image and show it
image = cv2.imread("New folder/215.jpg")
#orginal img
cv2.imshow("original", image)
#cropped img
cropped_up_up = image[0:165, 180:400]#image[20:180, 0:330] # supply startY and endY coordinates, startX and endX 70d(up):170i(down) 440d(l):540i(R)
cropped_right_right = image[135:340, 360:640] #image[60:190, 380:640]  # right right
cropped_left_left = image[140:340, 0:220] #image[180:480, 0:290]  # left left
cropped_down_down = image[310:480, 185:400] #image[180:480, 320:640]  # down down
cv2.imshow("cropped_up_up", cropped_up_up)
cv2.imshow('cropped_right_right ', cropped_right_right)
cv2.imshow('cropped_left_left ', cropped_left_left)
cv2.imshow('cropped_down_down ', cropped_down_down)

# write the cropped image to disk in PNG format
cv2.imwrite("cropped_img/up_up.jpg", cropped_up_up)
cv2.imwrite("cropped_img/down_down.jpg", cropped_down_down)
cv2.imwrite("cropped_img/left_left.jpg", cropped_left_left)
cv2.imwrite("cropped_img/right_right.jpg", cropped_right_right)

#cv2.waitKey(0)
#cropped = image[300:660, 600:1280]  # down down
#cropped = image[20:270, 0:570]  # up up
#cropped = image[50:360, 860:1280]  # right right
##cropped = image[250:600, 0:500]  # left left

#/////////////////////////////////////detection

 # Create the haar cascade
car_cascade = cv2.CascadeClassifier('mycars5.xml')

# Read the image
image_up_up = cv2.imread('cropped_img/up_up.jpg')
image_down_down = cv2.imread('cropped_img/down_down.jpg')
image_left_left = cv2.imread('cropped_img/left_left.jpg')
image_right_right = cv2.imread('cropped_img/right_right.jpg')

gray_up_up = cv2.cvtColor(image_up_up, cv2.COLOR_BGR2GRAY)
gray_down_down = cv2.cvtColor(image_down_down, cv2.COLOR_BGR2GRAY)
gray_left_left = cv2.cvtColor(image_left_left, cv2.COLOR_BGR2GRAY)
gray_right_right = cv2.cvtColor(image_right_right, cv2.COLOR_BGR2GRAY)

count_up_up = 0
count_down_down = 0
count_left_left = 0
count_right_right = 0

car_up_up =  car_cascade.detectMultiScale(gray_up_up, 1.1, 1)
car_down_down =  car_cascade.detectMultiScale(gray_down_down, 1.1, 1)
car_left_left =  car_cascade.detectMultiScale(gray_left_left, 1.1, 1)
car_right_right =  car_cascade.detectMultiScale(gray_right_right, 1.1, 1)

  # Draw a rectangle around the car
for (x, y, w, h) in car_up_up:
    cv2.rectangle(gray_up_up, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_up_up +=1

for (x, y, w, h) in car_down_down:
    cv2.rectangle(gray_down_down, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_down_down +=1

for (x, y, w, h) in car_left_left:
    cv2.rectangle(gray_left_left, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_left_left +=1

for (x, y, w, h) in car_right_right:
    cv2.rectangle(gray_right_right, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_right_right +=1

#cv2.imshow("car found", image_up_up)
cv2.imshow("gray_up_img", gray_up_up)

#cv2.imshow("car found", image_down_down)
cv2.imshow("gray_down_img", gray_down_down)

#cv2.imshow("car found", image_left_left)
cv2.imshow("gray_left_img", gray_left_left)

#cv2.imshow("car found", image_right_right)
cv2.imshow("gray_righr_img", gray_right_right)

status_up_up = cv2.imwrite('detected_cars/up_up.jpg', gray_up_up)
status_down_down = cv2.imwrite('detected_cars/down_down.jpg', gray_down_down)
status_left_left = cv2.imwrite('detected_cars/left_left.jpg', gray_left_left)
status_right_right = cv2.imwrite('detected_cars/right_right.jpg', gray_right_right)

print("Image car_up_up written to file-system : ", status_up_up)
print("Image car_down_down written to file-system : ", status_down_down)
print("Image car_left_left written to file-system : ", status_left_left)
print("Image car_right_right written to file-system : ", status_right_right)

print(count_up_up)
print(count_down_down)
print(count_left_left)
print(count_right_right)

#////////////////////accident detection

# Read the image
image_up_up = cv2.imread('cropped_img/up_up.jpg')
image_down_down = cv2.imread('cropped_img/down_down.jpg')
image_left_left = cv2.imread('cropped_img/left_left.jpg')
image_right_right = cv2.imread('cropped_img/right_right.jpg')

gray_up_up_acc = cv2.cvtColor(image_up_up, cv2.COLOR_BGR2GRAY)
gray_down_down_acc = cv2.cvtColor(image_down_down, cv2.COLOR_BGR2GRAY)
gray_left_left_acc = cv2.cvtColor(image_left_left, cv2.COLOR_BGR2GRAY)
gray_right_right_acc = cv2.cvtColor(image_right_right, cv2.COLOR_BGR2GRAY)

count_up_up_acc = 0
count_down_down_acc = 0
count_left_left_acc = 0
count_right_right_acc = 0

car_up_up_acc =  car_cascade.detectMultiScale(gray_up_up_acc, 1.1, 1)
car_down_down_acc =  car_cascade.detectMultiScale(gray_down_down_acc, 1.1, 1)
car_left_left_acc =  car_cascade.detectMultiScale(gray_left_left_acc, 1.1, 1)
car_right_right_acc =  car_cascade.detectMultiScale(gray_right_right_acc, 1.1, 1)

  # Draw a rectangle around the car
for (x, y, w, h) in car_up_up_acc:
    cv2.rectangle(gray_up_up_acc, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_up_up_acc +=1

for (x, y, w, h) in car_down_down_acc:
    cv2.rectangle(gray_down_down_acc, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_down_down_acc +=1

for (x, y, w, h) in car_left_left_acc:
    cv2.rectangle(gray_left_left_acc, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_left_left_acc +=1

for (x, y, w, h) in car_right_right_acc:
    cv2.rectangle(gray_right_right_acc, (x, y), (x+w, y+h), (0, 255, 0), 2)
    count_right_right_acc +=1

#cv2.imshow("car found", image_up_up)
#cv2.imshow("gray_up_img_acc", gray_up_up_acc)

#cv2.imshow("car found", image_down_down)
#cv2.imshow("gray_down_img_acc", gray_down_down_acc)

#cv2.imshow("car found", image_left_left)
#cv2.imshow("gray_left_img_acc", gray_left_left_acc)

#cv2.imshow("car found", image_right_right)
#cv2.imshow("gray_righr_img", gray_right_right)

status_up_up_acc = cv2.imwrite('detected_cars/up_up_acc.jpg', gray_up_up_acc)
status_down_down_acc = cv2.imwrite('detected_cars/down_down_acc.jpg', gray_down_down_acc)
status_left_left_acc = cv2.imwrite('detected_cars/left_left_acc.jpg', gray_left_left_acc)
status_right_right_acc = cv2.imwrite('detected_cars/right_right_acc.jpg', gray_right_right_acc)

print("Image car_up_up written to file-system : ", status_up_up_acc)
print("Image car_down_down written to file-system : ", status_down_down_acc)
print("Image car_left_left written to file-system : ", status_left_left_acc)
print("Image car_right_right written to file-system : ", status_right_right_acc)

#cv2.waitKey(0)
#////////////////////////////condetions for green and red signal

#active pins for led

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)


if (count_up_up_acc > 0) or (count_down_down_acc > 0) or (count_left_left_acc > 0) or (count_right_right_acc > 0):
    print("acceident occured")
    GPIO.output(31, True)
    GPIO.output(35, True)
    GPIO.output(26, True)
    GPIO.output(40, True)

# Driver Code
list1 = [count_up_up, count_down_down, count_left_left, count_right_right]


def Range(list1):
    largest = list1[0]
    lowest = list1[0]
    largest2 = None
    lowest2 = None
    for item in list1[1:]:
        if item > largest:
            largest2 = largest
            largest = item
        elif largest2 == None or largest2 < item:
            largest2 = item
        if item < lowest:
            lowest2 = lowest
            lowest = item
        elif lowest2 == None or lowest2 > item:
            lowest2 = item
    #print("Largest element is:", largest)
    #print("Smallest element is:", lowest)
    #print("Second Largest element is:", largest2)
    #print("Second Smallest element is:", lowest2)



    if list1[0] == 0:
        print("all red")
        GPIO.output(31,True)
        GPIO.output(35,True)
        GPIO.output(26,True)
        GPIO.output(40,True)

    if lowest == 0: # red on for all
        GPIO.output(31, True)
        GPIO.output(35, True)
        GPIO.output(26, True)
        GPIO.output(40, True)

    if lowest2 == 0: # red  for all
        GPIO.output(31, True)
        GPIO.output(35, True)
        GPIO.output(26, True)
        GPIO.output(40, True)

    if largest2 == 0: # red  for all
        GPIO.output(31, True)
        GPIO.output(35, True)
        GPIO.output(26, True)
        GPIO.output(40, True)


    if lowest > 0:
        if lowest == count_up_up:
            print("up low")
            GPIO.output(29, True)
            time.sleep(4)
            GPIO.output(31, True)
        if lowest == count_down_down:
            print("down low")
            GPIO.output(38, True)
            time.sleep(4)
            GPIO.output(40, True)
        if lowest == count_right_right:
            print("right low")
            GPIO.output(33, True)
            time.sleep(4)
            GPIO.output(35, True)
        if lowest == count_left_left:
            print("left low")
            GPIO.output(24, True)
            time.sleep(4)
            GPIO.output(26, True)

    if lowest2 > 0:
        if lowest2 == count_up_up:
            print("up avg")
            GPIO.output(29, True)
            time.sleep(8)
            GPIO.output(31, True)
        if lowest2 == count_down_down:
            print("down avg")
            GPIO.output(38, True)
            time.sleep(8)
            GPIO.output(40, True)
        if lowest2 == count_right_right:
            print("right avg")
            GPIO.output(33, True)
            time.sleep(8)
            GPIO.output(35, True)
        if lowest2 == count_left_left:
            print("left avg")
            GPIO.output(24, True)
            time.sleep(8)
            GPIO.output(26, True)

    if largest2 > 0:
        if largest2 == count_up_up:
            print("up medium")
            GPIO.output(29, True)
            time.sleep(12)
            GPIO.output(31, True)
        if largest2 == count_down_down:
            print("down medium")
            GPIO.output(38, True)
            time.sleep(12)
            GPIO.output(40, True)
        if largest2 == count_right_right:
            print("right medium")
            GPIO.output(33, True)
            time.sleep(12)
            GPIO.output(35, True)
        if largest2 == count_left_left:
            print("left medium")
            GPIO.output(24, True)
            time.sleep(12)
            GPIO.output(26, True)

    if largest > 0:
        if largest == count_up_up:
          print("up high")
          GPIO.output(29, True)
          time.sleep(16)
          GPIO.output(31, True)
        if largest == count_down_down:
          print("down high")
          GPIO.output(38, True)
          time.sleep(16)
          GPIO.output(40, True)
        if largest == count_right_right:
          print("right high")
          GPIO.output(33, True)
          time.sleep(16)
          GPIO.output(35, True)
        if largest == count_left_left:
          print("left high")
          GPIO.output(24, True)
          time.sleep(16)
          GPIO.output(26, True)



    if lowest == lowest2 == largest2 == largest:
        print("all are equal. so signal in clock wise direction")
        GPIO.output(24, True)
        time.sleep(5)
        GPIO.output(26, True)
        GPIO.output(29, True)
        time.sleep(5)
        GPIO.output(31, True)
        GPIO.output(33, True)
        time.sleep(5)
        GPIO.output(35, True)
        GPIO.output(38, True)
        time.sleep(5)
        GPIO.output(40, True)




Range(list1)
GPIO.cleanup()



cv2.waitKey(0)
cv2.destroyAllWindows()








              # to remove video and img

#os.remove("output.avi")  #remove of video
#os.remove("New folder")