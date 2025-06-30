from flask import Blueprint, render_template, request, make_response, g, session
from . import db
from .models import Tasks, User
from .rest import get_user
from uuid import uuid4

main = Blueprint('main', __name__)



@main.route('/')
def index():
    sess_id = request.cookies.get('sess_id')
    user = get_user()
    
    if not sess_id or len(sess_id) > 36:
        sess_id = str(uuid4())

    if user is None:
        sess_tasks = Tasks.query.filter_by(owner=sess_id, done=False).order_by(Tasks.id.desc()).all()
        sess_done = Tasks.query.filter_by(owner=sess_id, done=True).order_by(Tasks.id.desc()).all()
    else:
        sess_tasks, sess_done = user.tasks.filter_by(done=False).all(), user.tasks.filter_by(done=True).all()
    print(user)
    response = make_response(
        render_template('main.html', 
                        title='?', 
                        sess_id=sess_id,
                        sess_tasks=sess_tasks, 
                        sess_done=sess_done,
                        user=user)
    )
    
    response.set_cookie('sess_id', sess_id, max_age=31536000)

    return response

#TODO:


# Полное удаление задач с базы: по одной и удаление всего списка
# Изменение цвета задач