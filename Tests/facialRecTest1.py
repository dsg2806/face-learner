import cv2, os
import numpy as np
import dill
import pickle
from PIL import Image

#Things that make things work
arguments = ['haarcascade_frontalface_default.xml']
peopleIDs = []
idElement = 0

# Get user supplied values
cascPath = arguments[0]
faceCascade = cv2.CascadeClassifier(cascPath)

#Creates the face recogniser
recognizer = cv2.face.createLBPHFaceRecognizer()
peopleIDs = []
idElement = 0


#Teaches the recognizer based on images in the database
images = []
labels = []
for folder in os.walk('Database'):
    currentPerson = folder[0].split("\\")[-1]
    if (currentPerson!='Database'):#Nobody in the school can be named database now or else
        peopleIDs.append(idElement)#Also hopefully nobody's name is a number
        peopleIDs.append(currentPerson)
        for file in folder[2]:
            #Check and see if a face is detected in the image
            #First convert the image to grayscale
            image_pil = Image.open('Database\\'+currentPerson+'\\'+file).convert('L')
            image = np.array(image_pil, 'uint8')
            #Detect it
            faces = faceCascade.detectMultiScale(image)
            for (x, y, w, h) in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(idElement)
        idElement+=1
        print('Gathered files on '+currentPerson)

#Trains the recognizer
recognizer.train(images,np.array(labels))

#Things that make things work
arguments = ['haarcascade_frontalface_default.xml']

# Get user supplied values
cascPath = arguments[0]
faceCascade = cv2.CascadeClassifier(cascPath)

#Get the video thingy
video_capture = cv2.VideoCapture(1)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    #Make it all gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        #See if there's anyone we recognize in the rectangle
        recognize_image_pil = Image.fromarray(frame).convert('L')#.crop((x,y,x+w,y+h))#.convert('L')
        recognize_image = np.array(recognize_image_pil, 'uint8')

        person_predicted = recognizer.predict(recognize_image[y: y + h, x: x + w])#, confidence
        cv2.putText(frame, peopleIDs[peopleIDs.index(person_predicted)+1],(x,y),1,1,1)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    #Exit the script if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()