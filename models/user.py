from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from utils.config import get_role

class User (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    tickets = db.relationship(
        'Ticket',
        back_populates = 'author'
    )
    
    def __init__(self, username: str, email: str, password: str, role: str):
        self.__password_valitation(password)
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = get_role(role)
        
    def verify_password (self, password: str):
        return check_password_hash(self.password, password)
        
    def __password_valitation (self, raw_password: str):
        if len(raw_password) < 8:
            raise ValueError('The password must be at least 8 characters long.')
        if len(raw_password) > 30:
            raise ValueError('The password cannot be longer than 30 characters.')
        numbers = 0
        lower_alpha = 0
        upper_alpha = 0
        symbols = 0
        
        for char in raw_password:
            if char.isalpha():
                if char.islower():
                    lower_alpha += 1
                else:
                    upper_alpha += 1
            elif char.isnumeric():
                numbers += 1
            elif char in "@!¡*¿?()[]{}_-.#$%&":
                symbols += 1
        if not all(x > 0 for x in [numbers, lower_alpha, upper_alpha, symbols]):
            raise ValueError(
                'The password must contain at least one lowercase letter,one uppercase letter, one number, and one special character.'
            )
            
        