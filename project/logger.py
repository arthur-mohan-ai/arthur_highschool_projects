import datetime
from functools import wraps
import flask as F
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = db.Model

class RequestLogger(Base):
    __tablename__ = "request"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ip = db.Column(db.String(32))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    value = db.Column(db.String(32))

def logindatabase(f):
    @wraps(f)
    def inner(*args, **kwargs):
        r = RequestLogger()
        r.ip = F.request.remote_addr
        r.value = str(F.request.path)
        db.session.add(r)
        db.session.commit()
        return f(*args, **kwargs)
    return inner
