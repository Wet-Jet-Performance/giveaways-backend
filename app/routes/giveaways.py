from flask import Blueprint, request, current_app
from app import db
from app.models.giveaway import Giveaway
from app.models.photo import Photo
from base64 import encodebytes
from datetime import date
from PIL import Image
from werkzeug.utils import secure_filename
import io
import os

giveaways_bp = Blueprint("giveaways", __name__, url_prefix="/giveaways")

@giveaways_bp.route('', methods=['POST'])
def create_giveaway():
    request_body = dict(request.form)

    new_giveaway = Giveaway(name=request_body["name"],
                            start_date=request_body["start_date"],
                            end_date=request_body["end_date"]
                            )
    
    
    db.session.add(new_giveaway)
    db.session.commit()

    for photo in request.files.getlist('photos[]'):
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        new_photo = Photo(filename=filename, giveaway_id=new_giveaway.id)
        db.session.add(new_photo)
    db.session.commit()

    return {"msg": "Successfully created new Giveaway",
            "id": new_giveaway.id}, 201

@giveaways_bp.route('', methods=["GET"])
def get_giveaways():
    giveaways = db.session.scalars(db.select(Giveaway))

    return_giveaways = []

    for giveaway in giveaways:
        return_giveaways.append({
            "id": giveaway.id,
            "name": giveaway.name,
            "start_date": giveaway.start_date.strftime("%B %-d, %Y"),
            "end_date": giveaway.end_date.strftime("%B %-d, %Y"),
            "winners": [{
                "id": winner.id,
                "giveaway_id": winner.giveaway_id,
                "participant_id": winner.participant_id,
                "winning_ticket_id": winner.winning_ticket_id
            } for winner in giveaway.winners],
            "photos": [encode_photo(photo) for photo in giveaway.photos]
        })
    return return_giveaways, 200

@giveaways_bp.route('/<int:giveaway_id>', methods=["GET"])
def get_one_giveaway(giveaway_id):
    giveaway = db.session.scalar(db.select(Giveaway).where(Giveaway.id == giveaway_id))

    return_giveaway = {
            "name": giveaway.name,
            "id": giveaway.id,
            "start_date": giveaway.start_date.strftime("%B %-d, %Y"),
            "end_date": giveaway.end_date.strftime("%B %-d, %Y"),
            "winners": [{
                "id": winner.id,
                "giveaway_id": winner.giveaway_id,
                "participant_id": winner.participant_id,
                "winning_ticket_id": winner.winning_ticket_id
            } for winner in giveaway.winners]
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
    
    for winner in giveaway.winners:
        db.session.delete(winner)
    
    for ticket in giveaway.tickets:
        db.session.delete(ticket)

    for photo in giveaway.photos:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename))
        db.session.delete(photo)

    db.session.delete(giveaway)
    db.session.commit()

    return {"msg":f"Successfully deleted Giveaway with id {giveaway_id}"}, 200

def encode_photo(photo):
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], photo.filename)
    file_extension = photo.filename.rsplit('.', 1)[1].upper()
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format=file_extension) # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return (encoded_img, file_extension)