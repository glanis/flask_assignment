from db import db
import datetime

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    otp = db.Column(db.String)
    otp_sent = db.Column(db.DateTime)



    def __init__(self, username, password, email, otp):
        self.username = username
        self.password = password
        self.email = email
        self.otp = otp
        self.otp_sent = datetime.datetime.utcnow()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def json(self):
        return {'username': self.username}