from app import db
from .ticket import ticket
from .winner import winner

class Giveaway(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    participants = db.relationship('Participant', secondary=ticket, back_populates="giveaways_entered")
    winners = db.relationship('Participant', secondary=winner, back_populates='giveaways_won')