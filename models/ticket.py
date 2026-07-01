from utils.db import db
from datetime import datetime
from utils.config import TicketManagment

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    priority = db.Column(db.String(30), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, server_default = db.func.now())
    status = db.Column(db.String(30), nullable = False)
    finished_at = db.Column(db.DateTime)
    conclution = db.Column(db.Text())
    author = db.relationship(
        'User',
        back_populates='tickets'
        )
    
    def __init__(self, author_id, title, description, priority, status):
        self.author_id = author_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        
    def finish (self, conclution: str):
        self.conclution = conclution
        self.status = 'finished'
        self.finished_at = db.func.now()