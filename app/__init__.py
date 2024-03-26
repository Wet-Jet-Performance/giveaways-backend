from flask import Flask
# Step 1
# Import & Initialize SQL Alchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Initialize SQL Alchemy
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config = True):
    # __name__ store the name of the module we're in
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Step 2:
    # Configure SQLAlchemy
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_CONNECTION_STRING")
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("TEST_DATABASE_CONNECTION_STRING")

    # Import Models here!
    # from app.models.giveaway import Giveaway

    # Step 3:
    # Hook up Flask & Sql Alchemy
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.contact_info import ContactInfo
    from app.models.giveaway import Giveaway
    from app.models.giveaway_ticket import giveaway_ticket

    from .routes.giveaways import giveaways_bp
    app.register_blueprint(giveaways_bp)

    from .routes.contact_info import contact_info_bp
    app.register_blueprint(contact_info_bp)

    from .routes.giveaway_tickets import giveaway_tickets_bp
    app.register_blueprint(giveaway_tickets_bp)

    return app