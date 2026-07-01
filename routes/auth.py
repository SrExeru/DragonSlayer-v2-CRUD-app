from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.db import db
from models.user import User
from utils.auth import login_required, logout_required, user_can
from utils.config import Permissions

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
@login_required
@user_can('create_users')
def register_user ():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        try:
            if Permissions.roles[session['role']].hierarchy > Permissions.roles[role].hierarchy:
                raise ValueError('You cannot create users with a role higher than your own.')
            new_user = User(username, email, password, role)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('admin.menu'))
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('admin.menu'))
    
    return redirect(url_for('admin.menu'))

@auth.route('/login', methods=['POST', 'GET'])
@logout_required
def login_user ():
    if request.method == 'POST':
        user = db.session.query(User).filter_by(email=request.form.get('email')).first()
        
        if user is None or not user.verify_password(request.form.get('password')):
            return render_template(
                'login.html',
                title = 'Login',
                error = 'incorrect email or password.'
            )
        else:
            session['id'] = user.id
            session['role'] = user.role
            return redirect(url_for('main.home'))
        
    return render_template('login.html', title='Login')

@auth.route('/logout')
@login_required
def logout_user ():
    session.pop('id')
    return redirect(url_for('auth.login_user'))