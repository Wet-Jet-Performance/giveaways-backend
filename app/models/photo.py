from app import db
from .participant import Participant
from .giveaway import Giveaway

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String, nullable=False)
    giveaway_id = db.Column(db.Integer, db.ForeignKey(Giveaway.id))
    giveaway = db.relationship('Giveaway', back_populates="photos")