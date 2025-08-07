from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    bassin_longueur = db.Column(db.Float, nullable=False)
    mouvements_bras = db.Column(db.Integer, nullable=False)
    temps_total = db.Column(db.Float, nullable=False)
    bpm_instantane = db.Column(db.Float, nullable=False)


class Bassin(db.Model):
    __tablename__ = 'bassin'

    id = db.Column(db.Integer, primary_key=True)
    longueur = db.Column(db.Float, nullable=False)


# class BpmLog(db.Model):
#     __tablename__ = 'bpm_logs'

#     id = db.Column(db.Integer, primary_key=True)
#     session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=True)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     bpm = db.Column(db.Float)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):

        return check_password_hash(self.password_hash, password)
    
    
