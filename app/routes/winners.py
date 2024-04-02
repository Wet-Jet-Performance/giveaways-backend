from flask import Blueprint, request
from app import db
from app.models.winner import Winner

winners_bp = Blueprint("winners", __name__, url_prefix="/winners")

@winners_bp.route('', methods=["GET"])
def get_winners():
    winners = db.session.scalars(db.select(Winner))

    return_winners = []

    for winner in winners:
        return_winners.append({
            "id": winner.id,
            "giveaway_id": winner.giveaway_id,
            "participant_id": winner.participant_id
        })
    return return_winners, 200

@winners_bp.route('', methods=['POST'])
def create_winner():
    request_body = request.get_json()
    
    new_winner = Winner(giveaway_id=request_body["giveaway_id"],
                        participant_id=request_body["participant_id"])
    
    db.session.add(new_winner)
    db.session.commit()

    return {"msg":f"Successfully created new winner with id {new_winner.id}"}, 201