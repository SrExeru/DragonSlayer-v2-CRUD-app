from functools import wraps
from flask import session, redirect, url_for

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
            return redirect(url_for('auth.login_user'))
        return f(*args, **kwargs)
    return wrapper

def admin_required (f):
    @wraps(f)
    def wrapper (*args, **kwargs):
        if session.get('id') is None or session.get('role') not in ['administrator', 'owner']:
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return wrapper

def not_read_only (f):
    @wraps(f)
    def wrapper (*args, **kwargs):
        if session.get('id') is None or session.get('role') == 'read_only':
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return wrapper