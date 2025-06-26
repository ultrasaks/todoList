import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__, static_url_path="/assets", static_folder='assets')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .models import Tasks
    
    
    from .main import main as main_blueprint
    from .rest import rest as rest_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(rest_blueprint)
    
    migrate = Migrate(app, db)

    app.logger.handlers.clear()
    
    return app

app = create_app()

# from .models import Categories, Event