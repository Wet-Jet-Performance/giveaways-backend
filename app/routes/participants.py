from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.participant import Participant

participants_bp = Blueprint("participants", __name__, url_prefix="/participants")

@participants_bp.route('', methods=["GET"])
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

@participants_bp.route('', methods=['POST'])
def create_participant():
    request_body = request.get_json()

    new_participant = Participant(name=request_body["name"],
                            phone_number=request_body["phone_number"],
                            email=request_body["email"]
                            )
    
    db.session.add(new_participant)
    db.session.commit()

    return jsonify({"msg":f"Successfully created new participant contact info with id {new_participant.id}"}), 201