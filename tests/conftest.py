import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.giveaway import Giveaway
from app.models.participant import Participant
from app.models.ticket import Ticket
from app.models.winner import Winner
from app.models.photo import Photo

@pytest.fixture
def app():
    app = create_app(test_config=True)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_giveaways(app):
    giveaway1 = Giveaway(name="Giveaway 1",
                         description="This is a description.",
                         start_date="March 28, 2024", end_date="March 29, 2024")
    giveaway2 = Giveaway(name="Giveaway 2",
                         start_date="April 21, 2024", end_date="April 23, 2024")

    db.session.add(giveaway1)
    db.session.add(giveaway2)
    db.session.commit()

@pytest.fixture
def two_participants(app):
    participant1 = Participant(name="Participant 1", 
                         phone_number="(123)456-7890", email="participant1@email.com")
    participant2 = Participant(name="Participant 2",
                         phone_number="(123)456-7891", email="participant2@email.com")

    db.session.add(participant1)
    db.session.add(participant2)
    db.session.commit()

@pytest.fixture
def two_tickets(app):
    ticket1 = Ticket(giveaway_id=1, participant_id=1)
    ticket2 = Ticket(giveaway_id=1, participant_id=2)
    
    db.session.add(ticket1)
    db.session.add(ticket2)
    db.session.commit()

@pytest.fixture
def two_winners(app):
    winner1 = Winner(giveaway_id=1, participant_id=1, winning_ticket_id=1)
    winner2 = Winner(giveaway_id=1, participant_id=2, winning_ticket_id=2)
    
    db.session.add(winner1)
    db.session.add(winner2)
    db.session.commit()

@pytest.fixture
def two_photos(app):
    photo1 = Photo(giveaway_id=1, cloudflare_id="1")
    photo2 = Photo(giveaway_id=2, cloudflare_id="2")
    
    db.session.add(photo1)
    db.session.add(photo2)
    db.session.commit()

