from app import db
from datetime import datetime,timedelta

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')
    registration_time = db.Column(db.DateTime,nullable=False)

class VerificationCodeModel(db.Model):
    __tablename__ = "verification_code"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    code = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)

class LoginLogModel(db.Model):
    __tablename__ = "login_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)
