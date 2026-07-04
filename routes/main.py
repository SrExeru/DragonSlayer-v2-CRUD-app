from flask import Blueprint, render_template, redirect, session, url_for
from utils.auth import login_required, user_can
from utils.db import db
from models.user import User
from models.ticket import Ticket
from utils.config import TicketManagment, logged_show

main = Blueprint('main', __name__)

@main.route('/')
@login_required
@user_can('read_tickets')
def home ():
    return logged_show(
        'dashboard.html',
        title = 'Dashboard',
        style = url_for('static', filename = 'css/tickets.css'),
        script = url_for('static', filename = 'js/dashboard.js'),
        tickets = reversed(db.session.query(Ticket).all())
    )
    