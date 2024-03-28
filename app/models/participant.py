from app import db
from .ticket import ticket
from .winner import winner

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Text)
    email = db.Column(db.String)
    giveaways_entered = db.relationship('Giveaway', secondary=ticket, back_populates="participants")
    giveaways_won = db.relationship('Giveaway', secondary=winner, back_populates="winners")