from flask import Blueprint, request
from app import db
from app.models.ticket import Ticket

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")

@tickets_bp.route('', methods=['POST'])
def create_ticket():
    request_body = request.get_json()
    giveaway_id = request_body["giveaway_id"], 
    participant_id = request_body["participant_id"]
    num_tickets = int(request_body.get("number_of_tickets", 1))


    # if num_tickets == 1:
    #     new_ticket = Ticket(giveaway_id, participant_id)
    #     db.session.add(new_ticket)
    #     db.session.commit()
    # elif num_tickets > 1:
    
    new_tickets = [{"giveaway_id": giveaway_id, "participant_id": participant_id} for ticket in range(0, num_tickets)]
    
    db.session.execute(db.insert(Ticket), new_tickets)
    db.session.commit()


    return {"msg": "Successfully created new Ticket(s)"}, 201

@tickets_bp.route("", methods=["GET"])
def get_tickets():
    tickets = db.session.scalars(db.select(Ticket))

    return_tickets = []

    for ticket in tickets:
        return_tickets.append({
            "id": ticket.id,
            "giveaway_id": ticket.giveaway_id,
            "participant_id": ticket.participant_id,
            "giveaway_name": ticket.giveaway.name,
            "participant_name": ticket.participant.name,
            "participant_phone": ticket.participant.phone_number,
            "participant_email": ticket.participant.email
        })
    return return_tickets, 200

@tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_one_ticket(ticket_id):
    ticket = db.session.scalar(db.select(Ticket).where(Ticket.id == ticket_id))

    return_ticket = {
        "id": ticket.id,
        "giveaway_id": ticket.giveaway_id,
        "participant_id": ticket.participant_id,
        "giveaway_name": ticket.giveaway.name,
        "participant_name": ticket.participant.name,
        "participant_phone": ticket.participant.phone_number,
        "participant_email": ticket.participant.email
    }

    return return_ticket, 200

@tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    ticket = db.session.scalar(db.select(Ticket).where(Ticket.id == ticket_id))

    db.session.delete(ticket)
    db.session.commit()
    

    return {"msg":f"Successfully deleted Ticket with id {ticket_id}"}, 200


