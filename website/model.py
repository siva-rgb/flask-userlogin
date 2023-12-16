from website import db
# . means importing from current package which is website
from flask_login import UserMixin
from sqlalchemy import func

class Note(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    data= db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True), default=func.now())
    usr_id= db.Column(db.Integer, db.ForeignKey('user.id'))

# '''
# create user class that inherit db.Model and UserMixin 
# concept of multiple inhertance 
# '''
class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(150), unique=True)
    password= db.Column(db.String(150))
    user_name= db.Column(db.String(150))
    #we aslo need all the notes that a user has created so we need to define a relationship with notes
    # waht it will do it that it will kind of append all the notes of user that created by 1 user in a list
    # not exctly this is the backend structure of db structure but for understandig 
    # N must be capital while defining relationship
    notes= db.relationship('Note')



