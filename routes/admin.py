from flask import Blueprint, render_template, session, redirect, request, url_for, abort, flash, jsonify
from utils.auth import login_required, user_can, user_can_affect
from utils.db import db
from models.user import User
from utils.config import Permissions, logged_show
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['POST', 'GET'])
@login_required
@user_can('access_admin')
def menu ():
    users = db.session.query(User).all()
    
    return logged_show(
        'admin.html',
        title = 'Panel',
        style = url_for('static', filename = 'css/admin.css'),
        script = url_for('static', filename = 'js/admin.js'),
        users = users
    )
    
@admin.route('/user/<id>')
@login_required
@user_can('access_admin')
def user_info (id):
    user = db.session.query(User).filter_by(id = id).first()
    
    u_info = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'status': user.status
    }
    
    return jsonify(u_info)
    
@admin.route('/register', methods=['POST'])
@login_required
@user_can('create_user')
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

@admin.route('/edit', methods=['POST'])
@login_required
@user_can_affect('edit_user')
def edit_user ():
    if request.method == 'POST':
        id = request.form.get('id')
        
        user = db.session.query(User).filter_by(id = id).first()
        
        edited_username = request.form.get('username')
        edited_email = request.form.get('email')
        edited_role = request.form.get('role')
        edited_status = request.form.get('status')
        
        if Permissions.roles[session['role']].hierarchy > Permissions.roles[edited_role].hierarchy:
            abort(403)
        else:
            user.username = edited_username
            user.email = edited_email
            user.role = edited_role
            user.status = edited_status
            db.session.commit()
            
    return redirect(url_for('admin.menu'))
        
@admin.route('/reset_password', methods=['POST'])
@login_required
@user_can_affect('reset_password')
def reset_password ():
    if request.method == 'POST':
        id = request.form.get('id')
        user = db.session.query(User).filter_by(id = id).first()
        new_password = request.form.get('password')

        user.password = generate_password_hash(new_password)
        db.session.commit()
                
    return redirect(url_for('admin.menu'))
        