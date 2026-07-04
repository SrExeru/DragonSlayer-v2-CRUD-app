from flask import Blueprint, render_template, url_for, redirect, request, session, abort, jsonify
from utils.auth import login_required, user_can
from utils.db import db
from models.user import User
from models.ticket import Ticket

ticket = Blueprint('ticket', __name__, url_prefix='/ticket')

@ticket.route('/<id>')
@login_required
@user_can('read_tickets')
def obtain_ticket (id):
    t_required = db.session.query(Ticket).filter_by(id = id).first()
    t = {
        'id': t_required.id,
        'title': t_required.title,
        'description': t_required.description,
        'priority': t_required.priority,
        'status': t_required.status,
        'author': t_required.author.username,
        'created_at': t_required.created_at
    }
    return jsonify(t)

@ticket.route('/create', methods=['POST'])
@login_required
@user_can('create_ticket')
def create ():
    if request.method == 'POST':
        author_id = session.get('id')
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        status = request.form.get('status')
        
        new_ticket = Ticket(author_id, title, description, priority, status)
        
        db.session.add(new_ticket)
        db.session.commit()
        
        return redirect(url_for('main.home'))
    
    return redirect(url_for('main.home'))

@ticket.route('/edit', methods=['POST'])
@login_required
@user_can('edit_ticket')
def edit ():
    if request.method == 'POST':
        id = request.form.get('id')
        if id is None:
            abort(404)
        ticket = db.session.query(Ticket).filter_by(id = id).first()
        if ticket.status == 'finished':
            abort(403)
        if ticket is None:
            abort(404)
        else:
            ticket.title = request.form.get('title')
            ticket.description = request.form.get('description')
            ticket.priority = request.form.get('priority')
            
            db.session.commit()
    
    return redirect(url_for('main.home'))

@ticket.route('/finish/<id>', methods=['POST'])
@login_required
@user_can('conclude_ticket')
def finish (id):
    if request.method == 'POST':
        ticket = db.session.query(Ticket).filter_by(id = id).first()
        if ticket.status == 'finished':
            abort(403)
        if ticket is None:
            abort(404)
        else:
            ticket.finish(request.form.get('conclution'))
            db.session.commit()
    
    return redirect(url_for('main.home'))

