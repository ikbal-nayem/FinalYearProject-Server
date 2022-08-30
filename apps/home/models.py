from sqlalchemy_utils import UUIDType
from apps import db
import uuid


class Members(db.Model):

    __tablename__ = 'Members'

    id = db.Column(UUIDType(binary=False),
                   primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    gender = db.Column(db.String(10))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return f"{str(self.first_name)} {str(self.last_name)}"
