from flask import Flask, render_template as rt, request, redirect, url_for, session
from datetime import timedelta, date
from database.database import db
from database.models import *
import hashlib
from database.Utils import *


app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#All the routes for the app are here
@app.route('/')
def home():
    #If there is no session populate with none
    if session:
        todo_list=getUserTodos(session['userId'])
        lateTodos=getLateList(todo_list)
        user = session['user']
    else:
        todo_list = None
        user = None 
        lateTodos = None
    return rt('base.html',todo_list=todo_list, user=user, lateTodos=lateTodos)

@app.route('/login', methods=["GET","POST"])
def login():
        if request.method == "POST":
            username = request.form.get('email')
            password = request.form.get('password')
            #Check DB for user
            if validateLogin(username, password):
                session['user'] = username
                session['userId'] = getUserId(username)[0]
                return redirect(url_for("home"))
            else:
                return rt("login.html", error="Invalid Login")
         
        return rt("login.html")       

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route('/register', methods=["GET","POST"])
def register():
        if request.method == "POST":
            username = request.form.get('email')
            password = request.form.get('password')
            #Make sure an email address was sent
            if validateEmail(username):
                #salt the password
                salt = saltShaker()
                hashPass = hashlib.sha256((password+salt).encode('utf-8')).hexdigest()
                
                new_user = Users(username=username, password=hashPass, salt=salt)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
            return rt("register.html", error="Could Not Validate Email.")

         
        return rt("register.html")    

@app.route('/add',methods=['POST'])
def add():
    name = request.form.get("name")
    dueIn = request.form.get("dueDate")
    dayCreated = date.today()
    if dueIn != None:
        dueDate = dayCreated + timedelta(days=int(dueIn))
    else:
        dueDate = None
    new_task=Todo(name=name,done=False, userId=session['userId'], created=dayCreated, dueDate=dueDate)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo= Todo.query.get(todo_id)
    if session['userId'] == todo.userId:
        todo.done=not todo.done
        db.session.commit()
    return redirect(url_for("home"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo= Todo.query.get(todo_id)
    if session['userId'] == todo.userId:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)