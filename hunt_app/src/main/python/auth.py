import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from hunt_app.src.main.python.hunt_database import Team, save_object, update_object

bp = Blueprint('auth', __name__, url_prefix='/auth')


def register_auth_module(app):
    print("Registering authorisation module")
    app.register_blueprint(bp)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        team_name = request.form['username']
        captain = request.form['captain']
        password = request.form['password']
        error = None

        if not team_name:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not captain:
            error = 'Team Captain is required.'
        elif Team.query.filter_by(name=team_name).first() is not None:
            error = 'Team name already exists'

        if error is None:
            new_team = Team(name=team_name, captain=captain, login_code=generate_password_hash(password))
            save_object(new_team)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        team = Team.query.filter_by(name=username).first()

        if team is None:
            error = 'Team name is incorrect'
        elif not check_password_hash(team.login_code, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = Team.id
            return redirect(url_for('page.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Team.query.get(id=user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('page.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
