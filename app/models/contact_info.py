from app import db

class ContactInfo(db.Model):
    __tablename__ = "contact_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Text)
    email = db.Column(db.String)