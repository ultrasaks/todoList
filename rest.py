from flask import Blueprint, render_template, request
from . import db

rest = Blueprint('rest', __name__)

@rest.route('/new_task', methods=['POST'])
def new_tasker():
    data = request.get_json()
    print(data)
    q = data.get('name')
    return {"id": 1}


@rest.route('/del_task', methods=['POST'])
def del_tasker():
    data = request.get_json()
    return {"id": 1}