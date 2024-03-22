from flask import Blueprint, jsonify, request, abort, make_response
# from app import db
# from app.models.giveaway import Giveaway

giveaways_bp = Blueprint("giveaways", __name__, url_prefix="/giveaways")

@giveaways_bp.route('/')
def hello():
    return 'Hello, World!'