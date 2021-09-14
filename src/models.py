from flask_sqlalchemy import SQLAlchemy
from init import db


class camera_task(db.Model):
    __tablename__ = 'camera'
    id = db.Column('id', db.Integer, primary_key = True)
    start_time = db.Column('start_time', db.DateTime)
    end_time= db.Column('end_time', db.DateTime)
    duration = db.Column('duration', db.Float)
    
    def __init__(self, start_time, end_time, duration):
        self.start_time = start_time
        self.end_time= end_time
        self.duration = duration


class operation(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    start_time = db.Column('start_time', db.DateTime)
    end_time= db.Column('end_time', db.Integer)
    duration= db.Column('duration', db.Float)
    content = db.Column('content', db.String(50))
   
    def __init__(self, start_time, end_time, duration,content):
        self.start_time = start_time
        self.end_time= end_time
        self.duration = duration
        self.content = content
