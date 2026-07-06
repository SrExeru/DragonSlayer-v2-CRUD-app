from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import db
from models.user import User
from utils.auth import login_required, logout_required, user_can
from utils.config import Permissions

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
@logout_required
def login_user ():
    if request.method == 'POST':
        user = db.session.query(User).filter_by(email=request.form.get('email')).first()
        
        if user is None or not user.verify_password(request.form.get('password')):
            return render_template(
                'login.html',
                title = 'Login',
                style = url_for('static', filename = 'css/login.css'),
                error = 'incorrect email or password.'
            )
        elif user.status == 'inactive':
            return render_template(
                'login.html',
                title = 'Login',
                style = url_for('static', filename = 'css/login.css'),
                error = 'inactive user.'
            )
        else:
            session['id'] = user.id
            return redirect(url_for('main.home'))
        
    return render_template(
        'login.html',
        title = 'Login',
        style = url_for('static', filename = 'css/login.css')
    )

@auth.route('/logout')
@login_required
def logout_user ():
    session.clear()
    return redirect(url_for('auth.login_user'))