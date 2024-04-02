from app import db

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Text)
    email = db.Column(db.String)
    tickets = db.relationship("Ticket", back_populates="participant")
    giveaways_won = db.relationship("Winner", back_populates="participant")