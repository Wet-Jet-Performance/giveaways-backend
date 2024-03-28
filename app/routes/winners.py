from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.winner import winner

winners_bp = Blueprint("winners", __name__, url_prefix="/winners")

@winners_bp.route('', methods=["GET"])
def get_winners():
    winners = db.session.execute(db.select(winner))

    return_winners = []

    for entry in winners:
        return_winners.append({
            "id": entry[0],
            "giveaway_id": entry[1],
            "participant_id": entry[2]
        })
    return return_winners, 200

@winners_bp.route('', methods=['POST'])
def create_winner():
    request_body = request.get_json()
    
    result = db.session.execute(db.insert(winner).values(
                            giveaway_id=request_body["giveaway_id"],
                            participant_id=request_body["participant_id"]))
    
    db.session.commit()

    return jsonify({"msg":f"Successfully created new winner with id {result.inserted_primary_key[0]}"}), 201