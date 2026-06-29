from flask import Blueprint, render_template, session, redirect, request, url_for
from utils.auth import admin_required
from utils.db import db
from models.user import User
from utils.config import role_levels, get_role
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['POST', 'GET'])
@admin_required
def menu ():
    users = db.session.query(User).all()
    
    return render_template(
        'admin.html',
        title = 'Panel',
        users = users,
        roles = role_levels,
    )

@admin.route('/edit/<id>', methods=['POST'])
@admin_required
def edit_user (id):
    if request.method == 'POST':
        user = db.session.query(User).filter_by(id = id).first()
        edited_username = request.form.get('username')
        edited_email = request.form.get('email')
        edited_role = get_role(request.form.get('role'))
        
        if role_levels[session['role']] <= role_levels[edited_role]:
            pass
        else:
            user.username = edited_username
            user.email = edited_email
            user.role = edited_role
            db.session.commit()
    return redirect(url_for('admin.menu'))
        
@admin.route('/reset_password/<id>', methods=['POST'])
@admin_required
def reset_password (id):
    if request.method == 'POST':
        user = db.session.query(User).filter_by(id = id).first()
        new_password = request.form.get('password')
        
        if role_levels[session['role']] <= role_levels[user.role]:
            pass
        else:
            user.password = generate_password_hash(new_password)
            db.session.commit()
                
    return redirect(url_for('admin.menu'))