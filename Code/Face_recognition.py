import cv2, numpy, os
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
# loading classifier
face_cascade = cv2.CascadeClassifier(haar_file)
datasets = 'datasets'
print('Training...')

#initialization datasets
(images, labels, names, id) = ([], [], {}, 0)

# read the file from directory
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
            #print(labels)
        id += 1
# rezises files
(width, height) = (130, 100)

#making array for files
(images, labels) = [numpy.array(lis) for lis in [images, labels]]
#print(images, labels)

#initialize modifier/classifier
#model = cv2.face.LBPHFaceRecognizer_create()
model =  cv2.face.FisherFaceRecognizer_create()

#training model 
model.train(images, labels)
print ("training completed")

#initialize camera
webcam = cv2.VideoCapture(0)
cnt=0
while True:
    #reading camera
    (_, im) = webcam.read()
    #convert color img to gray img
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # detect the face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # loop for detected faces
    for (x,y,w,h) in faces:
        #reactangle around the faces
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
        #croped & perfectely match with dataset img
        face = gray[y:y + h, x:x + w]
        # face resize
        face_resize = cv2.resize(face, (width, height))

        # prediction
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
        # check the prediction is it valid or not
        if prediction[1]<800:
            cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0))
            print (names[prediction[0]])
            cnt=0
        else:
            cnt+=1
            cv2.putText(im,'Unknown',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 255))
            if(cnt>100):
                print("Unknown Person")
                cv2.imwrite("input.jpg",im)
                cnt=0
    #display            
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()
