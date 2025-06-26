from . import db

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100))
    description = db.Column(db.String(1024))
    deadline = db.Column(db.String(100))
    owner = db.Column(db.String(36))
    done = db.Column(db.Boolean, nullable=True, default=False)
    