import logging

from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from redis import StrictRedis
from sqlalchemy.sql.expression import func

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

db = SQLAlchemy()
redis_store = FlaskRedis.from_custom_provider(StrictRedis)

page = Blueprint('page', __name__)

def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('hunt_app.src.main.python.config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    db.init_app(app)
    redis_store.init_app(app)

    app.register_blueprint(page)
    app.logger.addHandler(stream_handler)

    return app


@page.route('/')
def index():
    if request.args.get('feed'):
        feed_count = redis_store.incr('feed_count')
        main_content = 'Feeding time'
    elif request.args.get('test_message'):
        main_content="Testing the main content insertion into the place."
    else:
        main_content = ''
        feed_count = redis_store.get('feed_count')
        if feed_count is None:
            feed_count = 0

    return render_template('index.html', feed_count=feed_count, main_content=main_content)


@page.route('/seed')
def seed():

    db.drop_all()
    db.create_all()

    test_team = Team(name="Team America", captain="James Runswick", login_code="123login", completion_percentage=25)
    db,session.add(test_team)
    db,session.commit()

    return redirect(url_for('page.index'))


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    captain = db.Column(db.Text())
    login_code = db.Column(db.Text())
    completion_percentage = db.Column(db.Integer)


class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    location = db.Column(db.Text())
    hint = db.Column(db.Text())
    puzzle = db.Column(db.Text())
    code_snippet = db.Column(db.Text())
