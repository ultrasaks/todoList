from flask import Blueprint, render_template, request, make_response
from . import db
from uuid import uuid4

main = Blueprint('main', __name__)

@main.route('/')
def index():
    sess_id = request.cookies.get('sess_id')
    
    if not sess_id or len(sess_id) > 36:
        sess_id = str(uuid4())
    
    sess_tasks = []
    sess_done = []
        
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


# Получение задач с сервера по сессии
# Добавление на сервер 
# Получение реального айди
# Удаление с сервера
# перенос скриптов из html-ки