from flask import Blueprint, request
from app import db
from app.models.giveaway import Giveaway
from datetime import date

giveaways_bp = Blueprint("giveaways", __name__, url_prefix="/giveaways")

@giveaways_bp.route('', methods=['POST'])
def create_giveaway():
    request_body = request.get_json()

    new_giveaway = Giveaway(name=request_body["name"],
                            start_date=request_body["start_date"],
                            end_date=request_body["end_date"]
                            )
    
    db.session.add(new_giveaway)
    db.session.commit()

    return {"msg":f"Successfully created new Giveaway with id {new_giveaway.id}"}, 201

@giveaways_bp.route('', methods=["GET"])
def get_giveaways():
    giveaways = db.session.scalars(db.select(Giveaway))

    return_giveaways = []

    for giveaway in giveaways:
        return_giveaways.append({
            "id": giveaway.id,
            "name": giveaway.name,
            "start_date": giveaway.start_date.strftime("%B %-d, %Y"),
            "end_date": giveaway.end_date.strftime("%B %-d, %Y")
        })
    return return_giveaways, 200

@giveaways_bp.route('/<int:giveaway_id>', methods=["GET"])
def get_one_giveaway(giveaway_id):
    giveaway = db.session.scalar(db.select(Giveaway).where(Giveaway.id == giveaway_id))

    return_giveaway = {
            "name": giveaway.name,
            "id": giveaway.id,
            "start_date": giveaway.start_date.strftime("%B %-d, %Y"),
            "end_date": giveaway.end_date.strftime("%B %-d, %Y")
        }

    return return_giveaway, 200

@giveaways_bp.route('/<int:giveaway_id>/tickets', methods=["GET"])
def get_giveaway_tickets(giveaway_id):
    giveaway = db.session.scalar(db.select(Giveaway).where(Giveaway.id == giveaway_id))

    return_tickets = []

    for ticket in giveaway.tickets:
        return_tickets.append({
            "id": ticket.id,
            "participant_id": ticket.participant_id,
            "giveaway_id": ticket.giveaway_id
        })

    return return_tickets, 200

@giveaways_bp.route('/<int:giveaway_id>/winners', methods=["GET"])
def get_giveaway_winners(giveaway_id):
    giveaway = db.session.scalar(db.select(Giveaway).where(Giveaway.id == giveaway_id))

    return_winners = []

    for winner in giveaway.winners:
        return_winners.append({
            "id": winner.id,
            "participant_id": winner.participant_id,
            "giveaway_id": winner.giveaway_id
        })

    return return_winners, 200


@giveaways_bp.route('/<int:giveaway_id>', methods=['PUT'])
def update_giveaway(giveaway_id):
    request_body = request.get_json()
    
    db.session.execute(db.update(Giveaway), [{
        "id": giveaway_id,
        "name": request_body["name"],
        "start_date": request_body["start_date"],
        "end_date": request_body["end_date"]
    }])

    db.session.commit()

    return {"msg":f"Successfully updated Giveaway with id {giveaway_id}"}, 200

@giveaways_bp.route('/<int:giveaway_id>', methods=['DELETE'])
def delete_giveaway(giveaway_id):
    giveaway = db.session.scalar(db.select(Giveaway).where(Giveaway.id == giveaway_id))
    for ticket in giveaway.tickets:
        db.session.delete(ticket)
    
    for winner in giveaway.winners:
        db.session.delete(winner)

    db.session.delete(giveaway)
    db.session.commit()

    return {"msg":f"Successfully deleted Giveaway with id {giveaway_id}"}, 200