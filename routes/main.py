from flask import Blueprint, render_template, redirect, session, url_for
from utils.auth import login_required
from utils.db import db
from models.user import User
from models.ticket import Ticket
from utils.config import priority_levels

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home ():
    user = db.session.query(User).filter_by(id = session['id']).first()
    return render_template(
        'dashboard.html',
        title = 'Dashboard',
        tickets = reversed(db.session.query(Ticket).all()),
        priority_levels = priority_levels
    )