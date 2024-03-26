from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.giveaway import Giveaway

giveaways_bp = Blueprint("giveaways", __name__, url_prefix="/giveaways")

@giveaways_bp.route('', methods=["GET"])
def get_giveaways():
    giveaways = db.session.scalars(db.select(Giveaway))

    return_giveaways = []

    for giveaway in giveaways:
        return_giveaways.append({
            "id": giveaway.id,
            "name": giveaway.name,
            "start_date_time": giveaway.start_date_time,
            "end_date_time": giveaway.end_date_time
        })
    return return_giveaways, 200

@giveaways_bp.route('', methods=['POST'])
def create_giveaway():
    request_body = request.get_json()

    new_giveaway = Giveaway(name=request_body["name"],
                            start_date_time=request_body["start_date_time"],
                            end_date_time=request_body["end_date_time"]
                            )
    
    db.session.add(new_giveaway)
    db.session.commit()

    return jsonify({"msg":f"Successfully created new Giveaway with id {new_giveaway.id}"}), 201