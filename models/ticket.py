from utils.db import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    priority = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, nullable = False, server_default = db.func.now())
    conclution = db.Column(db.Text())
    finished = db.Column(db.Boolean, default = False, nullable = False)
    author = db.relationship(
        'User',
        back_populates='tickets'
        )
    
    def __init__(self, author_id, title, description, priority):
        self.author_id = author_id
        self.title = title
        self.description = description
        self.priority = priority