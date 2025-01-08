import io
from bson import ObjectId
from flask import Blueprint, Response, jsonify, request, send_file
from models.mongoDBfile import MongoDBfile
from mongodb_api.phone_buddy_db import PhoneBuddyDB
# from services.firebase_auth import fb_auth

files = Blueprint("files", __name__)

# Maximum file size allowed (in bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@files.route("/file/<file_id>", methods=["GET"])
def get_file(file_id: str) -> Response:
    query = {"_id": ObjectId(file_id)}
    doc = PhoneBuddyDB.files_coll.find_one(query)
    if doc:
        obj = MongoDBfile.from_json(doc)
        return send_file(io.BytesIO(obj.file_bytes), mimetype=obj.file_type)
    else:
        return jsonify({"error": "File not found"})


# @fb_auth.login_required
@files.route("/file", methods=["PUT"])
def put_file() -> tuple[Response, int] | Response:

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and is_file_allowed(file.filename):
        file_bytes = file.read()
        file_size = len(file_bytes)

        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File size exceeds maximum limit (10MB)'}), 400

        created_file = MongoDBfile(ObjectId(), 'png', file_bytes)
        file_id = PhoneBuddyDB.files_coll.insert_one(created_file.to_json()).inserted_id
        return jsonify({"file_id": file_id}), 200
    return jsonify({'error': 'File type not allowed'}), 200


# @fb_auth.login_required
@files.route("/file/<file_id>", methods=["PATCH"])
def patch_file(file_id: str) -> tuple[Response, int] | Response:

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and is_file_allowed(file.filename):
        file_bytes = file.read()
        file_size = len(file_bytes)

        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File size exceeds maximum limit (10MB)'}), 400

        query = {"_id": ObjectId(file_id)}
        files_changed = PhoneBuddyDB.files_coll.update_one(query, {
            "$set": {
                "file_bytes": file_bytes
            }
        }).modified_count
        return jsonify({"files_changed": files_changed}), 200
    return jsonify({'error': 'File type not allowed'}), 200


# @fb_auth.login_required
@files.route("/file/<file_id>", methods=["DELETE"])
def delete_file(file_id: str) -> tuple[Response, int] | Response:
    query = {"_id": ObjectId(file_id)}
    result = PhoneBuddyDB.files_coll.delete_one(query)
    if result.deleted_count:
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "Can't Find File"}), 409


def is_file_allowed(filename):
    # Add any file extensions you want to allow here
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
