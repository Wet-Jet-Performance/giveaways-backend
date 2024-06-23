from app import db

class Giveaway(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    tickets = db.relationship("Ticket", back_populates="giveaway")
    winners = db.relationship("Winner", back_populates="giveaway")
    photos = db.relationship("Photo", back_populates="giveaway")