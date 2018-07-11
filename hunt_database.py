from flask_sqlalchemy import SQLAlchemy

init_db = SQLAlchemy()


class HuntDatabase:


    def __init__(self):
        database = SQLAlchemy()
        self.database = database


    def start_database(self, app):
        self.app = app
        self.database.init_app(app)


    def save_object(self, object):
        try:
            self.database.session.add(object)
            self.database.session.commit(object)
        except Exception as e:
            print("Exeception while create entry:  " + str(object)+ " Exception: " + str(e))


    def delete_object(self, object):
        try:
            self.database.session.remove(object)
            self.database.session.commit(object)
        except Exception as e:
            print("Exeception while create entry:  " + str(object)+ " Exception: " + str(e))


    def update_object(self, object):
        try:
            self.database.session.update(object)
            self.database.session.commit(object)
        except Exception as e:
            print("Exeception while create entry:  " + str(object)+ " Exception: " + str(e))


    def seed_database(self):
        print("Seeding database")
        self.database.drop_all()
        self.database.create_all()
        test_team = Team(name="Team America", captain="James Runswick", login_code="123login", completion_percentage=25)
        test_clue = Clue(name="Test Clue", location="Toyko", hint="Su shi", puzzle="What never forgets?", code_snippet="010 010110")
        self.database.session.add(test_team)
        self.database.session.add(test_clue)
        self.database.session.commit()


class Team(init_db.Model):
    id = init_db.Column(init_db.Integer, primary_key=True)
    name = init_db.Column(init_db.Text())
    captain = init_db.Column(init_db.Text())
    login_code = init_db.Column(init_db.Text())
    completion_percentage = init_db.Column(init_db.Integer)


class Clue(init_db.Model):
    id = init_db.Column(init_db.Integer, primary_key=True)
    name = init_db.Column(init_db.Text())
    location = init_db.Column(init_db.Text())
    hint = init_db.Column(init_db.Text())
    puzzle = init_db.Column(init_db.Text())
    code_snippet = init_db.Column(init_db.Text())


class SolvedClue(init_db.Model):
    team_id = init_db.Column(init_db.Text(), primary_key=True)
    clue_id = init_db.Column(init_db.Text(), primary_key=True)
    puzzle_solved = init_db.Column(init_db.Boolean)
