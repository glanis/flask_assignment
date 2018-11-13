from db import db


class ProfileModel(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),db.ForeignKey('users.username'))
    profession = db.Column(db.String(80))
    age = db.Column(db.Integer)
    address = db.Column(db.String(80))


    def __init__(self, name, profession, age, address):
        self.name = name
        self.profession = profession
        self.age = age
        self.address = address

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def json(self):
        return {'name': self.name, 'profession': self.profession, 'age': self.age, 'address': self.address}