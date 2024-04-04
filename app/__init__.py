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

    from .routes.giveaways import giveaways_bp
    app.register_blueprint(giveaways_bp)

    from .routes.participants import participants_bp
    app.register_blueprint(participants_bp)

    from .routes.tickets import tickets_bp
    app.register_blueprint(tickets_bp)

    from .routes.winners import winners_bp
    app.register_blueprint(winners_bp)

    # add origins parameter to specify where requests are allowed from
    # CORS(app, origins=[“http://localhost:8000”, “https://example.com”]).
    CORS(app)
    return app