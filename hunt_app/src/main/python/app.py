import logging

from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_redis import FlaskRedis
from redis import StrictRedis

from hunt_app.src.main.python.auth import register_auth_module
from hunt_app.src.main.python.hunt_database import start_database, seed_database

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

redis_store = FlaskRedis.from_custom_provider(StrictRedis)

page = Blueprint('page', __name__)

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('hunt_app.src.main.python.config.settings')
app.config.from_pyfile('settings.py', silent=True)


def create_app():

    redis_store.init_app(app)
    app.register_blueprint(page)
    app.logger.addHandler(stream_handler)
    register_auth_module(app)
    start_database(app)

    return app


@page.route('/')
def index():
    if request.args.get('feed'):
        feed_count = redis_store.incr('feed_count')
        main_content = 'Feeding time'
    elif request.args.get('test_message'):
        main_content = "Testing the main content insertion into the place."
        feed_count = 0
    else:
        main_content = ''
        feed_count = redis_store.get('feed_count')
        if feed_count is None:
            feed_count = 0

    return render_template('index.html', feed_count=feed_count, main_content=main_content)


@page.route('/seed')
def seed():
    seed_database()
    return redirect(url_for('page.index'))


