from flask import Flask, request, session, render_template, send_from_directory, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
import os
from PIL import Image



app = Flask(__name__)

  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://timotei:Timotei994@localhost:3306/db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)
    

    def __init__(self, id, photo, username, email):
        self.id = id
        self.username = username
        self.email = email
        

    def __repr__(self):
        return f"{self.id}; {self.username}, {self.email}."

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)
    message = db.Column(db.String(150), unique = True)

    def __init__(self, username, email, message):
        self.username = username
        self.email = email
        self.message = message

    def __repr__(self):
        return f"{self.username}, {self.email}, {self.message}."


"""" Upload Photo"""
UPLOADS_FOLDER = 'static/uploads/'
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER


""" CSS import """      
@app.route("/styl/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


""" Contact """
@app.route("/contact", methods = ['GET', 'POST'])
def contact():

    if request.method == 'POST':

        cont = Contact(
            request.form['username'],
            request.form['email'],
            request.form['message']
        )

        db.session.add(cont)
        db.session.commit()
        return 'Method was successful'
    else:
        return render_template("contact.html")


""" GET """
@app.route("/user", methods = ['GET'])
def get():

    user = Users.query.all()
    return render_template("render_get.html", content = user)


""" POST """
@app.route("/new_user", methods = ['POST', 'GET'])
def new_user():

    if request.method == "POST":
        usr = Users(
        request.form['id'],
        request.form['username'],
        request.form['email']
        )

        db.session.add(usr)
        db.session.commit()

        file = request.files['photo']
        file.save(os.path.join(app.config['UPLOADS_FOLDER'], file.filename))

        return 'Method POST was successful'
    else:
        return render_template("render_post.html")


""" PUT """
@app.route("/update/<id>", methods = ['POST', 'GET'])
def update(id):

    usr = Users.query.get_or_404(id)
    
    if request.method == 'POST':
        usr.id = request.form['id']
        usr.username = request.form['username']
        usr.email = request.form['email']
       
        db.session.add(usr)
        db.session.commit()
       
        return 'Method PUT was successful'
    else:
        return render_template("render_put.html", put = usr)


""" DELETE Method """
@app.route("/delete/<id>", methods = ['GET'])
def DELETE(id):
    
    
    user = Users.query.get_or_404(id)
    db.session.delete(user)        
    db.session.commit()
    return 'Method DELETE was successful'


if __name__ == "__main__":
    app.run(debug = True)