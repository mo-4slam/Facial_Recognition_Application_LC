from firebase import firebase
from main import name


#test file for sending data which was not used

firebase = firebase.FirebaseApplication(
    "https://face-recog-firebase-default-rtdb.firebaseio.com/", None)

data = {
    'Result': name
}

result = firebase.post('/face-recog-firebase-default-rtdb:/Result', data)
