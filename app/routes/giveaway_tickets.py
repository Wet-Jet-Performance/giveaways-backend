from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.giveaway_ticket import giveaway_ticket

giveaway_tickets_bp = Blueprint("giveaway_tickets", __name__, url_prefix="/giveaway_tickets")

@giveaway_tickets_bp.route('', methods=["GET"])
def get_giveaway_tickets():
    giveaway_tickets = db.session.execute(db.select(giveaway_ticket))

    return_giveaway_tickets = []

    for ticket in giveaway_tickets:
        print(ticket)
        return_giveaway_tickets.append({
            "id": ticket[0],
            "giveaway_id": ticket[1],
            "contact_id": ticket[2]
        })
    return return_giveaway_tickets, 200

@giveaway_tickets_bp.route('', methods=['POST'])
def create_giveaway_ticket():
    request_body = request.get_json()
    
    result = db.session.execute(db.insert(giveaway_ticket).values(
                            giveaway_id=request_body["giveaway_id"],
                            contact_id=request_body["contact_id"]))
    print(result)
    db.session.commit()

    return jsonify({"msg":f"Successfully created new Giveaway with id {result.inserted_primary_key[0]}"}), 201