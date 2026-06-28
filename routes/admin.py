from flask import Blueprint, render_template, session, redirect
from utils.auth import admin_required
from utils.db import db
from models.user import User
from utils.config import role_levels, get_role

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