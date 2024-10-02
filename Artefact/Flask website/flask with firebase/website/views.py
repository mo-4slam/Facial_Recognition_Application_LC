from flask import Blueprint, render_template
from flask_login import login_required, current_user
import pyrebase

views = Blueprint('views', __name__)

firebaseConfig = {
    "apiKey": "AIzaSyCiJpYEsddABDca-v81vSA5OWxY6JMAM0g",
    "authDomain": "face-recog-firebase.firebaseapp.com",
    "databaseURL": "https://face-recog-firebase-default-rtdb.firebaseio.com",
    "projectId": "face-recog-firebase",
    "storageBucket": "face-recog-firebase.appspot.com",
    "messagingSenderId": "1021160679237",
    "appId": "1:1021160679237:web:49ece1c8b10e125921402c"
}

# home page route


@views.route('/')
def home():
    return render_template("home.html", user=current_user)

# control panel route


@views.route('/control-panel')
@login_required
def control_panel():
    # within the control panel function firebase data is constantly retreived, so anytime the page is reloaded the data is retreived
    firebase = pyrebase.initialize_app(firebaseConfig)

    fb_db = firebase.database()

    name = fb_db.child("DATA").get()
    stringedname = str(name.val())
    stringedname
    for x in name.each():
        thing = x.key(), x.val()

    # some formatting of the data to make it look more appealing
    ting = str(thing)
    a = ting.replace("(", "")
    b = a.replace(")", "")
    c = b.replace("{", "")
    d = c.replace("}", "")
    e = d.replace(",", "\n")
    # render the html document using flask with (also retrieves what user is logged (user = current_user) in and the data (somedata = e))
    return render_template("control-panel1.html", user=current_user, somedata=e)

# learn more route


@views.route('/learn-more')
def learn_more():
    return render_template("learn_more.html", user=current_user)
