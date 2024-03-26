from app import db

class Giveaway(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    start_date_time = db.Column(db.DateTime)
    end_date_time = db.Column(db.DateTime)
    winning_entry_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'))

    #store photos in react public folder