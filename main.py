from flask import Blueprint, render_template, request, make_response
from . import db
from .models import Tasks
from uuid import uuid4

main = Blueprint('main', __name__)

@main.route('/')
def index():
    sess_id = request.cookies.get('sess_id')
    
    if not sess_id or len(sess_id) > 36:
        sess_id = str(uuid4())


    sess_tasks = Tasks.query.filter_by(owner=sess_id, done=False).order_by(Tasks.id.desc()).all()
    sess_done = Tasks.query.filter_by(owner=sess_id, done=True).order_by(Tasks.id.desc()).all()
        
    response = make_response(
        render_template('main.html', 
                        title='?', 
                        sess_id=sess_id,
                        sess_tasks=sess_tasks, 
                        sess_done=sess_done)
    )
    
    response.set_cookie('sess_id', sess_id, max_age=31536000)

    return response

#TODO:

# Модель аккаунта : имя, хеш пароля, (вирт) задачи в подчинении
# Вход с аккаунтом
# При создании аккаунта переносить задачи sess_id к новосозданному аккаунту
# ака обнулять задачи и ставить их во владение аккаунта
# Полное удаление задач с базы: по одной и удаление всего списка