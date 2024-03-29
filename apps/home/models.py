from sqlalchemy_utils import UUIDType
from datetime import datetime
from apps import db
import uuid


class Members(db.Model):
    __tablename__ = 'Members'

    id = db.Column(UUIDType(binary=False),
                   primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    number_of_dataset = db.Column(db.Integer())
    added_on = db.Column(db.DateTime(timezone=True), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return f"{str(self.first_name)} {str(self.last_name)}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Configuration(db.Model):
    __tablename__ = 'Configuration'

    id = db.Column(db.Integer, primary_key=True)
    rpi_ip = db.Column(db.String(64))
    rpi_username = db.Column(db.String(64))
    rpi_password = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return f"{str(self.rpi_ip)} {str(self.rpi_username)}"


class EntryLog(db.Model):
    __tablename__ = 'EntryLog'

    id = db.Column(db.Integer, primary_key=True)
    entry_time = db.Column(db.DateTime(timezone=True), default=datetime.now())
    confidance_level = db.Column(db.Float)
    member = db.Column(db.String(50))
    access_type = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            setattr(self, property, value)

    def __repr__(self):
        return f"{str(self.user_id)} {str(self.entry_time)}"
