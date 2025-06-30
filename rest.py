from flask import Blueprint, render_template, request, session
from . import db
from .models import Tasks, User

rest = Blueprint('rest', __name__)

def login_user(user):
    session.clear()
    session["user_id"] = user.id

def logout_user():
    session.clear()


@rest.route('/new_task', methods=['POST'])
def new_tasker():
    data = request.get_json()
    print(data)
    sess_id = request.cookies.get('sess_id')
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

@rest.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # Валидация
        if not username or not password:
            return '["Все поля обязательны.", "error"]'
        elif User.query.filter_by(username=username).first():
            return '["Такой пользователь уже существует.", "error"]'
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return '["Регистрация прошла успешно! Войдите.", "success"]'


@rest.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username_or_email).first().first()

        if user and user.check_password(password):
            login_user(user)
            return '["Вы вошли!", "success"]'
        else:
            return '["Неправильный логин или пароль.", "error"]'

    return render_template("login.html")

@rest.route("/logout")
def logout():
    logout_user()
    return 'Logout'