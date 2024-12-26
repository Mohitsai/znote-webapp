from datetime import datetime
from znote import db, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    tasks = db.relationship("Task", back_populates="user")

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', {self.username}', '{self.image_file}')"

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')

    def __repr__(self):
        return f"{self.name}"

user_roles = db.Table('user_roles',
                      db.Column('user_id', db.ForeignKey('users.id'), primary_key=True),
                      db.Column('roles_id', db.ForeignKey('roles.id'), primary_key=True))


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"Task('{self.description}')"
