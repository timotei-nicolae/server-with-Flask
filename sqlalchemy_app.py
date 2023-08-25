from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://timotei:Timotei994@localhost:3306/db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def __repr__(self):
        return f"{self.id}; {self.username}, {self.email}."


""" GET Method """
@app.route("/user", methods = ['GET'])
def get():

    string = """
    <!DOCTYPE html>
    <html>
    <body>

    <h2> Users table </h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            
        </tr>"""
    
    user = Users.query.all()
    
    for usr in user:
        string += """
        <tr>
            <td> %s </td>
            <td> %s </td>
            <td> %s </td>
            <td>
                <form action = "http://127.0.0.1:5000/update/%s" method = "GET">
                    <button> Update user</button>
                </form>
            <td>

            <td>
                <form action = "http://127.0.0.1:5000/delete/%s" method = "GET">
                    <button> Delete user </button>
                </form>
            <td>
            
        </tr>""" %(usr.id, usr.username, usr.email, usr.id, usr.id)
        
    string += """
    </table>  

    <form action = "http://127.0.0.1:5000/new_user" method = "GET">
        <button> Add user </button>
    </form>

    </body>
    </html>"""
    
    return string


""" POST Method """
@app.route("/new_user", methods = ['POST', 'GET'])
def new_user():

    form = """
    <html>
    <head>

        <title>Register Form</title>

    </head>
    <body>
    <form action = "http://127.0.0.1:5000/new_user" method = "POST">    
        <table>
            <tr>
                <td>Id:</td>
                <td>
                    <input type = "Id" placeholder="1, 2, 3......"   name="id"> 
                </td>
            </tr>
            <tr>
                <td>Username:</td>
                <td>
                    <input type = "text" placeholder="name"   name="username"> 
                </td>
            </tr>
            <tr>
                <td>Email:</td>
                <td>
                    <input type = "text" placeholder="email"   name="email"> 
                </td>
            </tr>
            
        </table>
            <button>Add</button>
    </form>
    </body>
    </html>
    """ 

    if request.method == "POST":
        usr = Users(
        request.form['id'],
        request.form['username'],
        request.form['email']
        )

        db.session.add(usr)
        db.session.commit()
        return 'Method POST was successful'
    else:
        return form


""" PUT Method """
@app.route("/update/<id>", methods = ['POST', 'GET'])
def update(id):

    usr = Users.query.get_or_404(id)

    update = """
    <html>
    <head>

        <title>Register Form</title>

    </head>
    <body>
    <form action = "http://127.0.0.1:5000/update/%s" method = "POST">    
        <table>
            <tr>
                <td>Id:</td>
                <td>
                    <input type = "Id"  name="id" value = "%s"> 
                </td>
            </tr>
            <tr>
                <td>Id:</td>
                <td>
                    <input type = "text"  name="username" value = "%s"> 
                </td>
            </tr>
            <tr>
                <td>Id:</td>
                <td>
                    <input type = "text"  name="email" value = "%s"> 
                </td>
            </tr>
        </table>

        <button>Go ahead!</button>
    </form>
        
    </body>
        
    </html>
    """%(usr.id, usr.id, usr.username, usr.email)
    
    if request.method == 'POST':
        usr.id = request.form['id']
        usr.username = request.form['username'],
        usr.email = request.form['email']
   
        db.session.add(usr)
        db.session.commit()
       
        return 'Method PUT was successful'
    else:
        return update

    
""" DELETE Method """
@app.route("/delete/<id>", methods = ['GET'])
def DELETE(id):
    
    
    user = Users.query.get_or_404(id)
    db.session.delete(user)        
    db.session.commit()
    return 'Method DELETE was successful'

if __name__ == "__main__":
    app.run(debug = True)