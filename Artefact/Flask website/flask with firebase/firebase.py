# file to test retrieving firebase data
import pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyCiJpYEsddABDca-v81vSA5OWxY6JMAM0g",
    "authDomain": "face-recog-firebase.firebaseapp.com",
    "databaseURL": "https://face-recog-firebase-default-rtdb.firebaseio.com",
    "projectId": "face-recog-firebase",
    "storageBucket": "face-recog-firebase.appspot.com",
    "messagingSenderId": "1021160679237",
    "appId": "1:1021160679237:web:49ece1c8b10e125921402c"
}

firebase = pyrebase.initialize_app(firebaseConfig)

fb_db = firebase.database()

datas = fb_db.child('DATA').get()

#data = datas[4]
#name = fb_db.child('DATA/Result').get()
names = []
name = fb_db.child("DATA").child().get()
names.append(name)
#last_record = fb_db.child('DATA').order_by_key().limit_to_last(1).get().val()
stringer = str(name.val())
stringer.replace(":", " ")

print(stringer)
# print(str(last_record))

# print(datas.val())
# print(data)
