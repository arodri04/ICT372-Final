from database.database import db

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    created = db.Column(db.String)
    dueDate = db.Column(db.String)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    
class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(20))
    salt = db.Column(db.String(10))
