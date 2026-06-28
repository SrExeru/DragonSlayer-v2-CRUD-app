from flask import Blueprint, render_template, url_for, redirect, request, session
from utils.auth import login_required, not_read_only
from utils.db import db
from models.user import User
from models.ticket import Ticket

ticket = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket.route('/create', methods=['POST'])
@not_read_only
def create ():
    if request.method == 'POST':
        author_id = session.get('id')
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        
        new_ticket = Ticket(author_id, title, description, priority)
        
        db.session.add(new_ticket)
        db.session.commit()
        
        return redirect(url_for('main.home'))
    
    return redirect(url_for('main.home'))

@ticket.route('/edit/<id>', methods=['POST'])
@not_read_only
def edit (id):
    if request.method == 'POST':
        ticket = db.session.query(Ticket).filter_by(id = id).first()
        if ticket is None:
            return redirect(url_for('main.home'))
        else:
            ticket.title = request.form.get('title')
            ticket.description = request.form.get('description')
            ticket.priority = request.form.get('priority')
            
            db.session.commit()
    
    return redirect(url_for('main.home'))

@ticket.route('/finish/<id>', methods=['POST'])
@not_read_only
def finish (id):
    if request.method == 'POST':
        ticket = db.session.query(Ticket).filter_by(id = id).first()
        if ticket is None:
            return redirect(url_for('main.home'))
        else:
            ticket.conclution = request.form.get('conclution')
            ticket.finished = True
            
            db.session.commit()
    
    return redirect(url_for('main.home'))

