from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.ticket import ticket

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")

@tickets_bp.route('', methods=["GET"])
def get_tickets():
    tickets = db.session.execute(db.select(ticket))

    return_tickets = []

    for entry in tickets:
        return_tickets.append({
            "id": entry[0],
            "giveaway_id": entry[1],
            "participant_id": entry[2]
        })
    return return_tickets, 200

@tickets_bp.route('', methods=['POST'])
def create_ticket():
    request_body = request.get_json()
    
    result = db.session.execute(db.insert(ticket).values(
                            giveaway_id=request_body["giveaway_id"],
                            participant_id=request_body["participant_id"]))
    
    db.session.commit()

    return jsonify({"msg":f"Successfully created new Ticket with id {result.inserted_primary_key[0]}"}), 201