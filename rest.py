from flask import Blueprint, render_template, request
from . import db
from .models import Tasks

rest = Blueprint('rest', __name__)

@rest.route('/new_task', methods=['POST'])
def new_tasker():
    data = request.get_json()
    print(data)
    sess_id = request.cookies.get('sess_id')
    #TODO: CHECK
    task = Tasks()
    task.title = data.get('name')
    task.description = data.get('description')
    task.deadline = data.get('datetime')
    if not task.deadline:
        task.deadline = 'нету'
    task.owner = sess_id
    
    db.session.add(task)
    db.session.commit()
    return {"id": task.id}


@rest.route('/del_task', methods=['POST'])
def del_tasker():
    data = request.get_json()
    sess_id = request.cookies.get('sess_id')
    task_id = int(data.get('id').replace('task_', ''))
    task = Tasks.query.filter_by(owner=sess_id, id=task_id).first()
    if task is not None:
        task.done = True
    db.session.add(task)
    db.session.commit()
    return {"id": task.id}