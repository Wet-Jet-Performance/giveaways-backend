from app import db
from .giveaway import Giveaway

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cloudflare_id = db.Column(db.String)
    giveaway_id = db.Column(db.Integer, db.ForeignKey(Giveaway.id))
    giveaway = db.relationship("Giveaway", back_populates="photos")