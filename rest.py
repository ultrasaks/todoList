from flask import Blueprint, render_template, request, session, redirect
from . import db
from .models import Tasks, User

rest = Blueprint('rest', __name__)


def get_user():
    user_id = session.get("user_id")
    return User.query.filter_by(id=user_id).first() if user_id is not None else None
    

def login_user(user):
    session.clear()
    session["user_id"] = user.id

def logout_user():
    session.clear()


@rest.route('/new_task', methods=['POST'])
def new_tasker():
    data = request.get_json()
    sess_id = request.cookies.get('sess_id')
    user = get_user()
    
    task = Tasks()
    task.title = data.get('name')
    task.description = data.get('description')
    task.deadline = data.get('datetime')
    if not task.deadline:
        task.deadline = 'нету'
    
    if user is None:
        task.owner = sess_id
    else:
        task.owner_id = user.id
    
    db.session.add(task)
    db.session.commit()
    return {"id": task.id}


@rest.route('/del_task', methods=['POST'])
def del_tasker():
    data = request.get_json()
    sess_id = request.cookies.get('sess_id')
    user = get_user()
    
    task_id = int(data.get('id').replace('task_', ''))
    if user is None:
        task = Tasks.query.filter_by(owner=sess_id, id=task_id).first()
    else:
        task = Tasks.query.filter_by(owner_id=user.id, id=task_id).first()
    
    if task is not None:
        task.done = True
    db.session.add(task)
    db.session.commit()
    return {"id": task.id}

@rest.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"].strip()
    password = data["password"]

    if not username or not password:
        return '["Все поля обязательны.", "error"]'
    elif User.query.filter_by(username=username).first():
        return '["Такой пользователь уже существует.", "error"]'
    else:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        sess_id = request.cookies.get('sess_id')
        for task in Tasks.query.filter_by(owner=sess_id).all():
            task.owner = None
            task.owner_id = user.id
            db.session.add(task)
            db.session.commit()
        
        return '["Регистрация прошла успешно! Войдите.", "success"]'


@rest.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"].strip()
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return '["Вы вошли!", "success"]'
        
    return '["Неправильный логин или пароль.", "error"]'

@rest.route("/logout")
def logout():
    logout_user()
    return redirect('/')