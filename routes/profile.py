from flask import Blueprint, render_template, session, redirect, request, url_for
from utils.db import db
from utils.auth import login_required, user_can
from models.user import User
from werkzeug.security import generate_password_hash
from utils.config import logged_show

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/', methods=['POST', 'GET'])
@login_required
def settings ():
    return logged_show(
        'settings.html',
        title = 'Profile',
        style = url_for('static', filename = 'css/profile.css')
    )
    
@profile.route('/change_username', methods=['POST'])
@login_required
@user_can('edit_self')
def change_username ():
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        user = db.session.query(User).filter_by(id = session['id']).first()
        same = db.session.query(User).filter_by(username = new_username).first()
        if same is not None:
            pass
        else:
            user.username = new_username
            db.session.commit()
        
    return redirect(url_for('profile.settings'))

@profile.route('/change_email', methods=['POST'])
@login_required
@user_can('edit_self')
def change_email ():
    if request.method == 'POST':
        new_email = request.form.get('new_email')
        user = db.session.query(User).filter_by(id = session['id']).first()
        same = db.session.query(User).filter_by(email = new_email).first()
        if same is not None:
            pass
        else:
            user.email = new_email
            db.session.commit()
        
    return redirect(url_for('profile.settings'))

@profile.route('/change_password', methods=['POST'])
@login_required
@user_can('edit_self')
def change_password ():
    if request.method == 'POST':
        password = request.form.get('actual_password')
        new_password = request.form.get('new_password')
        user = db.session.query(User).filter_by(id = session['id']).first()
        
        validation = user.verify_password(password)
        
        if not validation:
            return ('NO')
        else:
            user.password = generate_password_hash(new_password)
            db.session.commit()
        
    return redirect(url_for('profile.settings'))