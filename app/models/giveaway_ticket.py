from app import db

#Join Table
#1 row represents 1 ticket
giveaway_ticket = db.Table('giveaway_ticket',
                          db.Column('ticket_id', db.Integer, primary_key=True, autoincrement=True),
                          db.Column('giveaway_id', db.Integer, db.ForeignKey('giveaway.id')),
                          db.Column('contact_id', db.Integer, db.ForeignKey('contact_info.id')),
                          )