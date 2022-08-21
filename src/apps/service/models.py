# -*- encoding: utf-8 -*-

import datetime
from email.policy import default
from apps import db, login_manager

class OICalls(db.Model):

    __tablename__ = 'call'

    id = db.Column(db.Integer, primary_key=True)
    oi = db.Column(db.Float)
    change_oi = db.Column(db.Float)
    strike = db.Column(db.Integer)
    price = db.Column(db.Float)
    last_inserted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    

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
        return str(self.id)


class OIPuts(db.Model):

    __tablename__ = 'put'

    id = db.Column(db.Integer, primary_key=True)
    oi = db.Column(db.Float)
    change_oi = db.Column(db.Float)
    strike = db.Column(db.Integer)
    price = db.Column(db.Float)
    last_inserted = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
        return str(self.id)


class OI(db.Model):

    __tablename__ = 'oi'
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('call.id'))
    put_id = db.Column(db.Integer, db.ForeignKey('put.id'))
    expiry = db.Column(db.Date)

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
        return str(self.id)

# @login_manager.user_loader
# def user_loader(id):
#     return OICalls.query.filter_by(id=id).first()

