from app import db
from .participant import Participant
from .giveaway import Giveaway
from .ticket import Ticket

class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    winning_ticket_id = db.Column(db.Integer, db.ForeignKey(Ticket.id))
    giveaway_id = db.Column(db.Integer, db.ForeignKey(Giveaway.id))
    participant_id = db.Column(db.Integer, db.ForeignKey(Participant.id))
    participant = db.relationship('Participant', back_populates="giveaways_won")
    giveaway = db.relationship('Giveaway', back_populates="winners")