from flask import Blueprint, request
from app import db
from app.models.photo import Photo
import os
import requests

photos_bp = Blueprint("photos", __name__, url_prefix="/photos")
account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
api_token = os.environ.get("CLOUDFLARE_API_TOKEN")

@photos_bp.route('/photo-upload', methods=['GET'])
def get_photo_upload_url():
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v2/direct_upload"
    data = {"metadata": {"key": "value"}, "requireSignedURLs": "false"}
    headers = {
        'Authorization': f"Bearer {api_token}"
      }
    response = requests.post(url, files={}, headers=headers)

    return response.json(), response.status_code

@photos_bp.route('', methods=['POST'])
def create_photo():
    request_body = request.get_json()

    new_photo = Photo(cloudflare_id=request_body["cloudflare_id"],
                            giveaway_id=request_body["giveaway_id"]
                            )
    
    
    db.session.add(new_photo)
    db.session.commit()
    return {"msg": "Successfully created new Photo",
            "id": new_photo.id}, 201


@photos_bp.route('', methods=["GET"])
def get_photos():
    photos = db.session.scalars(db.select(Photo))

    return_photos = []

    for photo in photos:
        return_photos.append({
            "id": photo.id,
            "cloudflare_id": photo.cloudflare_id
        })

    return return_photos, 200

@photos_bp.route('/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    photo = db.session.scalar(db.select(Photo).where(Photo.id == photo_id))

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/{photo.cloudflare_id}"

    headers = {
        'Authorization': f"Bearer {api_token}"
      }
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        db.session.delete(photo)
        db.session.commit()

        return {"msg":f"Successfully deleted photo with id {photo_id}"}, 200
    else:
        return {"msg": f"Failed to delete photo with id {photo_id}"}, 500