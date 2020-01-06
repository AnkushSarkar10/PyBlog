from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import click
from flask.cli import with_appcontext
import os

# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(__name__)

# app.config['SECRET_KEY'] = '9wql9ae7831413470949afcb024zxc6'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'twitter.login'
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

app.cli.add_command(create_tables)

from app import views