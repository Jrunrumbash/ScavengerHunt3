import logging
from flask import Blueprint, Flask, jsonify, render_template, redirect, request, url_for, json
from flask_redis import FlaskRedis
from redis import StrictRedis

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
redis_store = FlaskRedis.from_custom_provider(StrictRedis)
page = Blueprint('page', __name__)
app = Flask(__name__, instance_relative_config=True)
team_db = {}


def create_app():


    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    redis_store.init_app(app)

    # app.register_blueprint(page)
    app.logger.addHandler(stream_handler)

    return app

@app.route('/addTeam', methods=['POST'])
def addTeam():
    team_name = request.form.get('team_name')
    team_captain = request.form.get('captain')
    password = request.form.get('password')
    if team_name and team_captain and password:
        new_team = Team(team_name, team_captain, password)
        team_db[team_name] = new_team
        print(team_db)
        return jsonify(new_team.__dict__)
    return "Registration Failed"


@app.route('/login', methods=['POST'])
def login():
    team_name = request.form.get('team_name')
    password = request.form.get('password')
    if team_name:
        team_to_query = team_db[team_name]
        if password == team_to_query.password:
            return "Login Successful"
        else:
            return "Incorrect Password"
    return "Login Failed"



class Team():
    def __init__(self, team_name, team_captain, password):
        self.team_name = team_name
        self.captain = team_name
        self.password = password
