import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import re
from helpers import login_required

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, IMAGES, configure_uploads
import uuid


# Configure application
app = Flask(__name__)

# Learnt some of flask_limiter functionalities from Youtube and google
#limiter = Limiter(key_func=get_remote_address)
#limiter.init_app(app)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# CSRF protection
app.config['SECRET_KEY'] ='amongusisagoodgameec94289df0be2af712e949f0e7cd6a1c3bdf19c0b95c77a8478ac9e48aa0c430andthisisasecretkey'


# configuration for image uploading using flask_uploads
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.root_path, 'static/uploads')
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(app.root_path, 'static/uploads')
configure_uploads(app, photos)




# make the form in which the "finders" will upload the items
class UploadFoundItem(FlaskForm):
    photo = FileField ("Upload an Image", validators = [FileAllowed(IMAGES, "Images only are accepted")])
    Title = StringField("Upload a title", validators = [DataRequired()])
    location = StringField("Where did you find the item?", validators = [DataRequired()])
    description = TextAreaField("Upload a description")
    question1 = StringField("First Question")
    question2 = StringField("Second Question")
    question3 = StringField("Third Question")
    submit = SubmitField('Upload')




def save_item(user_id, photo, Title, location, description, question1, question2, question3):
    original_filename = secure_filename(photo.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    photos.save(photo, name = unique_filename)
    db.execute("INSERT INTO ITEMS (user_id, picture, title, location, description, question1, question2, question3) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                user_id, unique_filename, Title, location, description, question1, question2, question3)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


##########################################################################################################################################

@app.route("/")
@login_required
def index():
    items = db.execute("SELECT * FROM items")
    return render_template("index.html", items = items)


##########################################################################################################################################

@app.route("/login", methods=["GET", "POST"])
#limit login requests to 5 per day to prevent brute forcing
#@limiter.limit('5 per hour')
def login():

    if request.method == "POST":
        session.clear()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        if not email:
            flash("please provide an Email")
            return redirect("/login")

        # the following check came from Chat GPT to prevent SQL injection attacks and check for valid email format

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            flash("Invalid email format")
            return redirect("/login")

        if not password:
            flash("please provide a password")
            return redirect("/login")

        row = db.execute("SELECT * FROM users WHERE email = ?", email)

        if (not row != 1 or not check_password_hash(row[0]["hash"] ,password)):
            flash("Invalid Email and/or Password")
            return redirect("/login")

        #debug account:   admin@gmail.com    admin1234

        session["user_id"] = row[0]["id"]
        return redirect("/choice")



    elif request.method == "GET":

        return render_template("login.html")
############################################################################################################################
@app.route("/choice", methods=["GET", "POST"])
@login_required
def choice():
    if request.method == "POST":
        session.clear()
        return redirect("/login")

    elif request.method == "GET":
        return render_template("choice.html")

############################################################################################################################

@app.route("/found", methods=["GET", "POST"])
@login_required
def found():

    form = UploadFoundItem()

    if form.validate_on_submit():
        Title = form.Title.data
        form.Title.data = None
        photo = form.photo.data
        form.photo.data = None
        location = form.location.data
        form.location.data = None
        description = form.description.data
        form.description.data = None
        question1 = form.question1.data
        form.question1.data = None
        question2 = form.question2.data
        form.question2.data = None
        question3 = form.question3.data
        form.question3.data = None

        user_id = session["user_id"]
        save_item(user_id, photo, Title, location, description, question1, question2, question3)
        flash("Item Uploaded successfully")




    return render_template("found.html",
                            form = form)

############################################################################################################################
@app.route("/register", methods=["GET", "POST"])

def register():
    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirmation = request.form.get("confirmation").strip()

        if not email:
            flash("please provide an Email")
            return redirect("/register")

        # the following check came from Chat GPT to prevent SQL injection attacks and check for valid email format

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            flash("Invalid email format")
            return redirect("/register")

        if not password:
            flash("please provide a password")
            return redirect("/register")

        if not confirmation:
            flash("please confirm your password")
            return redirect("/register")

        if confirmation != password:
            flash("confirmation doesn't match the entered password")
            return redirect("/register")

        if not check_pass(password):
            flash("please use a stronger password containing at least 1 symbol, 1 number and 8 characters minimum")
            return redirect("/register")

        for user in db.execute("SELECT email FROM users"):
            if email == user['email']:
                    flash("email already in use")
                    return redirect("/register")

        db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, generate_password_hash(password))

        return redirect("/choice")


    else:
        return render_template("register.html")

############################################################################################################################

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

############################################################################################################################

@app.route("/viewingpage")
@login_required
def view():

    item_info = db.execute("SELECT * FROM items WHERE id == ?", request.args.get("item_id"))
    return render_template("viewingpage.html", info = item_info)

