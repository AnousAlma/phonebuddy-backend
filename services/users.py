from bson import ObjectId
from flask import Blueprint, Response, jsonify, request
from models.user import User
from mongodb_api.phone_buddy_db import PhoneBuddyDB
# from services.firebase_auth import fb_auth
from utils.FirebaseAPI import FirebaseAPI

users = Blueprint("/users", __name__)


@users.route("/user", methods=["PUT"])
# @fb_auth.login_required
def create_user() -> tuple[Response, int]:
    res = request.get_json()['user']
    res['_id'] = str(ObjectId())
    user = User.from_json(res)
    user.email = user.email.lower()
    query = {"email": user.email}
    existing_user = PhoneBuddyDB.users_coll.find_one(query)
    if existing_user is None:
        user_data = user.to_json()
        inserted_id = PhoneBuddyDB.users_coll.insert_one(user_data).inserted_id
        PhoneBuddyDB.users_coll.update_one(query, {"$set": {"archived": False}})
        user_data = User.from_json(PhoneBuddyDB.users_coll.find_one({"_id": ObjectId(inserted_id)})).to_json()
        return jsonify({"user": user_data}), 200
    else:
        return jsonify({"error": "User already exists with same email, please log in"}), 400


@users.route("/user/<user_id>", methods=["GET"])
# @fb_auth.login_required
def get_user(user_id: str) -> tuple[Response, int]:
    query = {"_id": ObjectId(user_id), "archived": False}
    item = PhoneBuddyDB.users_coll.find_one(query)
    if not item:
        return jsonify({"error": "user not found"}), 404

    item = User.from_json(item)
    return jsonify({"user": item}), 200



@users.route("/user/auth", methods=["GET"])
# @fb_auth.login_required
def login() -> tuple[Response, int]:
    user = FirebaseAPI.get_user(request.headers.get('Authorization').split(' ')[1])
    if user is None:
        return jsonify({"error": "user not found"}), 404

    query = {"_id": ObjectId(user.oid), "archived": False}
    item = PhoneBuddyDB.users_coll.find_one(query)
    if not item:
        return jsonify({"error": "user not found"}), 404

    item = User.from_json(item)
    return jsonify({"user": item}), 200


@users.route("/user/<user_id>", methods=["PATCH"])
# @fb_auth.login_required
def update_user(user_id: str) -> tuple[Response, int]:
    user_data = User.from_json(request.get_json()).to_json()
    query = {"_id": ObjectId(user_id), "archived": False}
    updated = PhoneBuddyDB.users_coll.find_one_and_update(query, {"$set": user_data}, return_document=True)
    if updated:
        item = User.from_json(updated)
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 400


@users.route("/user/<user_id>", methods=["DELETE"])
# @fb_auth.login_required
def delete_user(user_id: str) -> tuple[Response, int]:
    query = {"_id": ObjectId(user_id), "archived": False}
    update_result = PhoneBuddyDB.users_coll.update_one(query, {"$set": {"archived": True}})
    if update_result.modified_count:
        return jsonify({"message": "User archived successfully"}), 200
    else:
        return jsonify({"error": "User not found or already archived"}), 400
