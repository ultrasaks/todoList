from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100))
    description = db.Column(db.String(1024))
    deadline = db.Column(db.String(100))
    owner = db.Column(db.String(36))
    done = db.Column(db.Boolean, nullable=True, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pw_hash = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Tasks', backref='user', lazy='dynamic')

    def set_password(self, password: str) -> None:
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pw_hash, password)