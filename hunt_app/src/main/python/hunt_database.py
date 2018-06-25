from flask_sqlalchemy import SQLAlchemy

model_database = SQLAlchemy()


def start_database(app):
    print("Starting database")
    model_database.init_app(app)


def save_object(database_entry_object):
    try:
        model_database.session.add(database_entry_object)
        model_database.session.commit()
    except Exception as e:
        print("Exception while create entry:  " + str(database_entry_object) + " Exception: " + str(e))


def delete_object(database_entry_object):
    try:
        model_database.session.remove(database_entry_object)
        model_database.session.commit()
    except Exception as e:
        print("Exception while create entry:  " + str(database_entry_object) + " Exception: " + str(e))


def update_object(database_entry_object):
    try:
        model_database.session.update(database_entry_object)
        model_database.session.commit()
    except Exception as e:
        print("Exception while create entry:  " + str(database_entry_object) + " Exception: " + str(e))


def seed_database():
    print("Seeding database")
    model_database.drop_all()
    model_database.create_all()
    test_team = Team(name="Team America", captain="James Runswick", login_code="123login", completion_percentage=25)
    test_clue = Clue(name="Test Clue", location="Toyko", hint="Su shi", puzzle="What never forgets?",
                     code_snippet="010 010110")
    save_object(test_team)
    save_object(test_clue)


class Team(model_database.Model):
    id = model_database.Column(model_database.Integer, primary_key=True)
    name = model_database.Column(model_database.String(80))
    captain = model_database.Column(model_database.String(80))
    login_code = model_database.Column(model_database.Text)
    completion_percentage = model_database.Column(model_database.Integer)


class Clue(model_database.Model):
    id = model_database.Column(model_database.Integer, primary_key=True)
    name = model_database.Column(model_database.Text())
    location = model_database.Column(model_database.Text())
    hint = model_database.Column(model_database.Text())
    puzzle = model_database.Column(model_database.Text())
    code_snippet = model_database.Column(model_database.Text())


class SolvedClue(model_database.Model):
    id = model_database.Column(model_database.Integer, primary_key=True)
    team_id = model_database.Column(model_database.Integer, model_database.ForeignKey('team.id'))
    clue_id = model_database.Column(model_database.Integer, model_database.ForeignKey('clue.id'))
    puzzle_solved = model_database.Column(model_database.Boolean)
