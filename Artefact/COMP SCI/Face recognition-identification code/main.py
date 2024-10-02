#from anyio import current_time
import numpy as np
import cv2
import pickle
from firebase import firebase
import datetime

firebase = firebase.FirebaseApplication(
    "https://face-recog-firebase-default-rtdb.firebaseio.com/", None)

now = datetime.datetime.today().strftime("%Y%m%d%H%M")

capture = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()


labels = {"person_name": 1}


with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}
recognizer.read("trainner.yml")


def make_1080p():
    capture.set(3, 1920)
    capture.set(4, 1080)


def make_720p():
    capture.set(3, 1280)
    capture.set(4, 720)


def make_480p():
    capture.set(3, 640)
    capture.set(4, 480)


def change_res(width, height):
    capture.set(3, width)
    capture.set(4, height)


make_480p()
change_res(480, 360)

face_cascade = cv2.CascadeClassifier(
    'src/cascades/data/haarcascade_frontalface_alt2.xml')

font = cv2.FONT_HERSHEY_SIMPLEX
color = (255, 255, 255)
stroke = 2


while True:
    ret, frame = capture.read()
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detectmultiscale is getting a (x,y,w,h) value for the face, using the haar cascade referenced above
    faces = face_cascade.detectMultiScale(
        grayframe, scaleFactor=1.5, minNeighbors=5)
    # here we are referencing the co ordinates retrieved earlier, and defining a region of interest so that we can "imwrite" the roi
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        roi_gray = grayframe[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)
        if conf >= 0 and conf <= 50:
            print(id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1,
                        color, stroke, cv2.LINE_AA)
            data = {
                'Result': name,
                'Timestamp': now
                }
            result = firebase.post('/DATA/', data)


        else:
            cv2.putText(frame, "Unknown", (x, y), font,
                        1, color, stroke, cv2.LINE_AA)
            data={
                'Result': 'Unkown',
                'Timestamp': now
            }
            firebase.post('/DATA/',data)

        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_gray)
        color = (255, 0, 0)  # BGR
        stroke = 2
        end_cord_x = x+w
        end_cord_y = y+h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    # display
    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
print(cv2.__version__)
