from flask import Blueprint, request
from app import db
from app.models.ticket import Ticket

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")

@tickets_bp.route('', methods=['POST'])
def create_ticket():
    request_body = request.get_json()
    
    new_ticket = Ticket(giveaway_id=request_body["giveaway_id"], 
                        participant_id=request_body["participant_id"])
    
    db.session.add(new_ticket)
    db.session.commit()

    return {"msg":f"Successfully created new Ticket with id {new_ticket.id}"}, 201

@tickets_bp.route("", methods=["GET"])
def get_tickets():
    tickets = db.session.scalars(db.select(Ticket))

    return_tickets = []

    for ticket in tickets:
        return_tickets.append({
            "id": ticket.id,
            "giveaway_id": ticket.giveaway_id,
            "participant_id": ticket.participant_id
        })
    return return_tickets, 200
