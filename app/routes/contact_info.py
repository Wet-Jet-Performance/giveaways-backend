from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.contact_info import ContactInfo

contact_info_bp = Blueprint("contact_info", __name__, url_prefix="/contact_info")

@contact_info_bp.route('', methods=["GET"])
def get_contact_info():
    all_contacts = db.session.scalars(db.select(ContactInfo))

    return_contact_info = []

    for contact_info in all_contacts:
        return_contact_info.append({
            "id": contact_info.id,
            "name": contact_info.name,
            "phone_number": contact_info.phone_number,
            "email": contact_info.email
        })
    return return_contact_info, 200

@contact_info_bp.route('', methods=['POST'])
def create_contact_info():
    request_body = request.get_json()

    new_contact_info = ContactInfo(name=request_body["name"],
                            phone_number=request_body["phone_number"],
                            email=request_body["email"]
                            )
    
    db.session.add(new_contact_info)
    db.session.commit()

    return jsonify({"msg":f"Successfully created new participant contact info with id {new_contact_info.id}"}), 201