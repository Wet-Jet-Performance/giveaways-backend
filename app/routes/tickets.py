from flask import Blueprint, request, current_app, render_template
from flask_mail import Mail, Message
from app import db
from app.models.ticket import Ticket
from app.models.participant import Participant
from app.models.giveaway import Giveaway
import os

tickets_bp = Blueprint("tickets", __name__, url_prefix="/tickets")

@tickets_bp.route('', methods=['POST'])
def create_ticket():
    request_body = request.get_json()
    giveaway_id = request_body["giveaway_id"] 
    participant_id = request_body["participant_id"]
    num_tickets = int(request_body.get("number_of_tickets", 1))
    
    new_tickets = [{"giveaway_id": giveaway_id, "participant_id": participant_id} for ticket in range(0, num_tickets)]
    
    new_tickets = db.session.scalars(db.insert(Ticket).returning(Ticket), new_tickets)
    db.session.commit()
    return_ids = [ticket.id for ticket in new_tickets]

    return {"msg": "Successfully created new Ticket(s)",
            "ids": return_ids}, 201

@tickets_bp.route('/email', methods=['POST'])
def send_email():
    request_body = request.get_json()
    giveaway_id = request_body["giveaway_id"]
    participant_id = request_body["participant_id"]
    ticket_ids = request_body["ticket_ids"]

    participant = db.session.scalar(db.select(Participant).where(Participant.id == participant_id))
    giveaway = db.session.scalar(db.select(Giveaway).where(Giveaway.id == giveaway_id))
    total_tickets = db.session.scalars(db.select(Ticket).where((Ticket.giveaway_id == giveaway_id) & (Ticket.participant_id == participant_id))).all()


    mail = Mail(current_app)
    msg = Message(
        subject='New Tickets Added for WJP Giveaway', 
        sender=os.environ.get("GMAIL_ACCOUNT"), 
        recipients=[participant.email],
        html=render_template('new_tickets_email.html', participant_name=participant.name, giveaway_name=giveaway.name, number_of_tickets=len(ticket_ids), ticket_ids=ticket_ids, total_tickets=len(total_tickets))
    )
    mail.send(msg)


    return {"msg": "Email sent successfully"}, 200

# Only fetches 10000 tickets due to timeout and frontend can't handle more than 10000 tickets
@tickets_bp.route("", methods=["GET"])
def get_tickets():
    tickets = db.session.query(Ticket)\
                        .order_by(Ticket.id.desc())\
                        .limit(1000000)\
                        .all()
    
    # tickets = db.session.query(Ticket).order_by(Ticket.id.desc()).all()


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


