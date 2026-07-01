from functools import wraps
from flask import session, redirect, url_for, abort, request
from utils.config import Permissions
from utils.db import db
from models.user import User

def login_required (f):
    @wraps(f)
    def wrapper (*args, **kwargs):
        if session.get('id') is None:
            return redirect(url_for('auth.login_user'))
        return f(*args, **kwargs)
    return wrapper

def logout_required (f):
    @wraps(f)
    def wrapper (*args, **kwargs):
        if session.get('id') is not None:
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return wrapper

def user_can (*perms):
    def decorator (f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = db.session.query(User).filter_by(id = session.get('id')).first()
            for perm in perms:
                if not Permissions.can(user, perm):
                    abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
        
def user_can_affect (*perms):
    def decorator (f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            author = db.session.query(User).filter_by(id = session.get('id')).first()
            affected = db.session.query(User).filter_by(id = request.view_args.get('id')).first()
            if affected is None:
                abort(404)
            for perm in perms:
                if not Permissions.can_affect(perm, author, affected):
                    abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator