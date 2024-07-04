from app import db


class GiveawaySteps(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_number = db.Column(db.String)
    step_title = db.Column(db.String)
    step_description = db.Column(db.String)