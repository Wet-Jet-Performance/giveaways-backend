from flask import Blueprint, request, jsonify
from app import db
from app.models.giveawaysteps import GiveawaySteps

giveawaysteps_bp = Blueprint("giveawaysteps", __name__, url_prefix="/giveawaysteps")

@giveawaysteps_bp.route('', methods=['POST'])
def create_dynamicdata():
    request_body = request.get_json()
    new_giveawaystep = GiveawaySteps(
        step_number=request_body["step_number"],
        step_title=request_body.get("step_title", None),
        step_description=request_body["step_description"],
    )
    
    db.session.add(new_giveawaystep)
    db.session.commit()
    
    response_data = {
        "id": new_giveawaystep.id,
        "step_number": new_giveawaystep.step_number,
        "step_title": new_giveawaystep.step_title,
        "step_description": new_giveawaystep.step_description,
    }
    
    return jsonify({
        "msg": "Successfully added new data",
        "data": response_data
    }), 201

@giveawaysteps_bp.route('', methods=['GET'])
def get_all_giveawaysteps():
    giveawaysteps = GiveawaySteps.query.all()
    response_data = [
        {
            "id": step.id,
            "step_number": step.step_number,
            "step_title": step.step_title,
            "step_description": step.step_description
        }
        for step in giveawaysteps
    ]
    
    return jsonify(response_data), 200

@giveawaysteps_bp.route('/<int:id>', methods=['DELETE'])
def delete_giveawaystep(id):
    giveawaystep = GiveawaySteps.query.get(id)
    if giveawaystep is None:
        return jsonify({"msg": "Giveaway step not found"}), 404
    
    db.session.delete(giveawaystep)
    db.session.commit()
    
    return jsonify({"msg": "Giveaway step successfully deleted"}), 200
