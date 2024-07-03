from flask import Blueprint, request, jsonify
from app import db
from app.models.dynamicdata import DynamicData

dynamicdata_bp = Blueprint("dynamicdata", __name__, url_prefix="/dynamicdata")

@dynamicdata_bp.route('', methods=['POST'])
def create_dynamicdata():
    request_body = request.get_json()
    new_dynamicdata = DynamicData(
        title=request_body["title"],
        description=request_body.get("description", None),
        image_url=request_body["image_url"],
    )
    
    db.session.add(new_dynamicdata)
    db.session.commit()
    
    # Serialize the new_dynamicdata object to a dictionary
    response_data = {
        "id": new_dynamicdata.id,
        "title": new_dynamicdata.title,
        "description": new_dynamicdata.description,
        "image_url": new_dynamicdata.image_url,
    }
    
    return jsonify({
        "msg": "Successfully added new data",
    }), 201


@dynamicdata_bp.route('', methods=['GET'])
def get_dynamicdata():
    # Get all DynamicData records
    dynamicdata_list = DynamicData.query.all()
    
    # Serialize the data to a list of dictionaries
    response_data = [{
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "image_url": item.image_url
    } for item in dynamicdata_list]
    
    return jsonify(response_data), 200

@dynamicdata_bp.route('/<int:id>', methods=['DELETE'])
def delete_dynamicdata(id):
    # Get a DynamicData record by its ID
    dynamicdata = DynamicData.query.get(id)
    
    if dynamicdata is None:
        return jsonify({"msg": "DynamicData not found"}), 404
    
    db.session.delete(dynamicdata)
    db.session.commit()
    
    return jsonify({"msg": "Successfully deleted DynamicData"}), 200
