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
            "participant_id": winner.participant_id,
            "winning_ticket_id": winner.winning_ticket_id,
            "participant_name": winner.participant.name,
            "participant_phone": winner.participant.phone_number,
            "participant_email": winner.participant.email
        })
    return return_winners, 200

@winners_bp.route('', methods=['POST'])
def create_winner():
    request_body = request.get_json()
    
    new_winner = Winner(giveaway_id=request_body["giveaway_id"],
                        participant_id=request_body["participant_id"],
                        winning_ticket_id=request_body["winning_ticket_id"])
    
    db.session.add(new_winner)
    db.session.commit()

    return {"msg": "Successfully created new winner",
            "id": new_winner.id}, 201

@winners_bp.route("/<int:winner_id>", methods=["GET"])
def get_one_winner(winner_id):
    winner = db.session.scalar(db.select(Winner).where(Winner.id == winner_id))

    return_winner = {
        "id": winner.id,
        "giveaway_id": winner.giveaway_id,
        "participant_id": winner.participant_id,
        "winning_ticket_id": winner.winning_ticket_id,
        "participant_name": winner.participant.name,
        "participant_phone": winner.participant.phone_number,
        "participant_email": winner.participant.email
    }

    return return_winner, 200

@winners_bp.route("/<int:winner_id>", methods=["DELETE"])
def delete_winner(winner_id):
    winner = db.session.scalar(db.select(Winner).where(Winner.id == winner_id))

    db.session.delete(winner)
    db.session.commit()
    

    return {"msg":f"Successfully deleted Winner with id {winner_id}"}, 200