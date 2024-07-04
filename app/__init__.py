from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os


db = SQLAlchemy()
migrate = Migrate()
load_dotenv(override=True)


def create_app(test_config = False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.environ.get("GMAIL_ACCOUNT")
    app.config['MAIL_PASSWORD'] = os.environ.get("GMAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("GMAIL_ACCOUNT")

    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONNECTION_STRING")
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DATABASE_CONNECTION_STRING")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.participant import Participant
    from app.models.giveaway import Giveaway
    from app.models.ticket import Ticket
    from app.models.winner import Winner
    from app.models.photo import Photo
    from app.models.dynamicdata import DynamicData
    from app.models.giveawaysteps import GiveawaySteps

    from .routes.giveaways import giveaways_bp
    app.register_blueprint(giveaways_bp)

    from .routes.participants import participants_bp
    app.register_blueprint(participants_bp)

    from .routes.tickets import tickets_bp
    app.register_blueprint(tickets_bp)

    from .routes.winners import winners_bp
    app.register_blueprint(winners_bp)

    from .routes.photos import photos_bp
    app.register_blueprint(photos_bp)

    from .routes.dynamicdata import dynamicdata_bp
    app.register_blueprint(dynamicdata_bp)

    from .routes.giveawaystep import giveawaysteps_bp
    app.register_blueprint(giveawaysteps_bp)

    # add origins parameter to specify where requests are allowed from
    # CORS(app, origins=[“http://localhost:8000”, “https://example.com”]).

    CORS(app, origins=["https://wetjetperformancegiveaways.onrender.com","http://localhost:3000"])

    return app