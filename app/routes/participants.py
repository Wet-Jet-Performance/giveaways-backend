from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.participant import Participant

participants_bp = Blueprint("participants", __name__, url_prefix="/participants")

@participants_bp.route("", methods=["GET"])
def get_participants():
    participants = db.session.scalars(db.select(Participant))

    return_participants = []

    for participant in participants:
        return_participants.append({
            "id": participant.id,
            "name": participant.name,
            "phone_number": participant.phone_number,
            "email": participant.email
        })
    return return_participants, 200

@participants_bp.route("", methods=["POST"])
def create_participant():
    request_body = request.get_json()

    new_participant = Participant(name=request_body["name"],
                            phone_number=request_body["phone_number"],
                            email=request_body["email"]
                            )
    
    db.session.add(new_participant)
    db.session.commit()

    return jsonify({"msg":f"Successfully created new participant contact info with id {new_participant.id}"}), 201

@participants_bp.route("/<int:participant_id>", methods=["GET"])
def get_one_participant(participant_id):
    participant = db.session.scalar(db.select(Participant).where(Participant.id == participant_id))

    return_participant = {
            "id": participant.id,
            "name": participant.name,
            "phone_number": participant.phone_number,
            "email": participant.email
            }
    return return_participant, 200


@participants_bp.route("/<int:participant_id>/giveaways_entered", methods=["GET"])
def get_participant_giveaways(participant_id):
    participant = db.session.scalar(db.select(Participant).where(Participant.id == participant_id))

    return_giveaways = []

    for giveaway in participant.giveaways_entered:
        return_giveaways.append({
            "name": giveaway.name,
            "id": giveaway.id,
            "start_date": giveaway.start_date,
            "end_date": giveaway.end_date
        })

    return return_giveaways, 200

@participants_bp.route('/<int:participant_id>', methods=['PUT'])
def update_participant(participant_id):
    request_body = request.get_json()
    
    db.session.execute(db.update(Participant), [{
        "id": participant_id,
        "name": request_body["name"],
        "phone_number": request_body["phone_number"],
        "email": request_body["email"]
    }])

    db.session.commit()

    return {"msg":f"Successfully updated Participant with id {participant_id}"}, 200

@participants_bp.route('/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    participant = db.session.scalar(db.select(Participant).where(Participant.id == participant_id))
    
    db.session.delete(participant)

    db.session.commit()

    return {"msg":f"Successfully deleted Participant with id {participant_id}"}, 200