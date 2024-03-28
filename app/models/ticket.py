from app import db

#Join Table
#1 row represents 1 ticket
ticket = db.Table('ticket',
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('giveaway_id', db.Integer, db.ForeignKey('giveaway.id')),
                    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id')),
                    )