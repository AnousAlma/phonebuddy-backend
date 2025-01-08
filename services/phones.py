import bson
from bson import ObjectId
from flask import Blueprint, Response, jsonify, request
from models.phone import Phone
from mongodb_api.phone_buddy_db import PhoneBuddyDB
# from services.firebase_auth import fb_auth

phones = Blueprint("phone", __name__)


@phones.route("/phone", methods=["PUT"])
# @fb_auth.login_required
def create_phone() -> tuple[Response, int]:

    phone_data = request.get_json()['phone']
    phone_data['_id'] = str(bson.ObjectId())
    phone = Phone.from_json(phone_data)
    inserted_id = PhoneBuddyDB.phones_coll.insert_one(phone.to_json()).inserted_id
    phone = Phone.from_json(PhoneBuddyDB.phones_coll.find_one({"_id": inserted_id}))
    return jsonify({"phone": phone}), 200

@phones.route("/phone", methods=["GET"])
def get_phones():
    # Get query parameters
    filters = request.args.to_dict()
    page = int(filters.get("page", 1))
    limit = int(filters.get("limit", 20))
    sort = filters.get("sort", "featured")

    # Build the MongoDB query
    query = {}
    if filters.get("brands") and filters["brands"] != "all":
        query["brand"] = filters["brands"]
    if filters.get("providers") and filters["providers"] != "all":
        query["provider"] = filters["providers"]

    # print(query)

    # Query the database
    total_phones = PhoneBuddyDB.phones_coll.count_documents(query)
    if sort == "price-ascending":
        phones = (
            PhoneBuddyDB.phones_coll.find(query)
            .sort("monthly", 1)
            .skip((page - 1) * limit)
            .limit(limit)
        )
    elif sort == "price-descending":
        phones = (
            PhoneBuddyDB.phones_coll.find(query)
            .sort("monthly", -1)
            .skip((page - 1) * limit)
            .limit(limit)
        )
    else:
        phones = (
            PhoneBuddyDB.phones_coll.find(query)
            .skip((page - 1) * limit)
            .limit(limit)
        )
    phones = [Phone.from_json(phone) for phone in phones]

    # Calculate total pages
    curr_phone = ((page - 1) * limit) + 1
    last_phone = curr_phone + limit - 1
    if last_phone > total_phones:
        last_phone = total_phones
    message = f"Showing {curr_phone} - {last_phone} of {total_phones}"
    total_pages = (total_phones + limit - 1) // limit

    return jsonify({"phones": phones, "message": message, "totalPages": total_pages}), 200


@phones.route("/phone/<phone_id>", methods=["GET"])
# @fb_auth.login_required
def get_phone(phone_id: str) -> tuple[Response, int]:
    query = {"_id": ObjectId(phone_id)}
    phone_doc = PhoneBuddyDB.phones_coll.find_one(query)
    if phone_doc:
        phone = Phone.from_json(phone_doc)
        PhoneBuddyDB.phones_coll.find_one_and_update(query, {"$set": phone.to_json()}, return_document=True)
        return jsonify({"phone": phone}), 200
    else:
        print("Phone not found")
        return jsonify({"error": "Phone not found"}), 400


@phones.route("/phone/<phone_id>", methods=["PATCH"])
# @fb_auth.login_required
def update_phone(phone_id: str) -> tuple[Response, int]:
    phone_data = request.get_json()
    query = {"_id": ObjectId(phone_id)}
    phone_data["_id"] = ObjectId(phone_id)
    phone_data["brand"] = ObjectId(phone_data["brand"])
    phone_data["phone"] = ObjectId(phone_data["phone"])
    phone_data["monthly"] = ObjectId(phone_data["monthly"])
    phone_data["upfront"] = ObjectId(phone_data["upfront"])
    phone = phone_data.from_json(PhoneBuddyDB.phones_coll.find_one({"_id": ObjectId(phone_data)}))

    updated = PhoneBuddyDB.phones_coll.find_one_and_update(query, {"$set": phone_data}, return_document=True)
    if updated:
        phone = Phone.from_json(updated)
        return jsonify(phone.to_json()), 200
    else:
        return jsonify({"error": "Phone not found"}), 400


@phones.route("/phone/<phone_id>", methods=["DELETE"])
# @fb_auth.login_required
def delete_phone(phone_id: str) -> tuple[Response, int]:
    query = {"_id": ObjectId(phone_id)}
    result = PhoneBuddyDB.phones_coll.delete_one(query)
    if result.deleted_count:
        return jsonify({"message": "Phone successfully deleted"}), 200
    else:
        return jsonify({"error": "Phone not found or already deleted"}), 400
