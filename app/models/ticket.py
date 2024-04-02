from app import db
from .participant import Participant
from .giveaway import Giveaway

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    giveaway_id = db.Column(db.Integer, db.ForeignKey(Giveaway.id))
    participant_id = db.Column(db.Integer, db.ForeignKey(Participant.id))
    participant = db.relationship('Participant', back_populates="tickets")
    giveaway = db.relationship('Giveaway', back_populates="tickets")

