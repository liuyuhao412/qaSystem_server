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

    def to_json(self):
        time = self.registration_time
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            'id': self.id,
            'username':self.username,
            'email':self.email,
            'role':self.role,
            'registration_time':time,
        }


class VerificationCodeModel(db.Model):
    __tablename__ = "verification_code"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    code = db.Column(db.String(255), nullable=False)
    is_valid= db.Column(db.String(10), default='有效')
    created_time = db.Column(db.DateTime, nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        time = datetime.utcnow() + timedelta(hours=8)
        if self.expiration_time < time:
            self.is_valid = '无效'
        created_time = self.created_time
        created_time = created_time.strftime("%Y-%m-%d %H:%M:%S")
        expiration_time = self.expiration_time
        expiration_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            'id': self.id,
            'email':self.email,
            'code':self.code,
            'is_valid':self.is_valid,
            'created_time':created_time,
            'expiration_time':expiration_time,
        }
        


class LoginLogModel(db.Model):
    __tablename__ = "login_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    ip = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        time = self.login_time
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            'id': self.id,
            'username':self.username,
            'role':self.role,
            'ip':self.ip,
            'login_time':time,
        }
