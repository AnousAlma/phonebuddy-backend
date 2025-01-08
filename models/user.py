"""
User Model
"""

from __future__ import annotations
import json
from typing import Optional
from models.abstract_db_model import DB_MODEL
from bson import ObjectId


class User(DB_MODEL):
    oid: ObjectId
    full_name: str
    email: str
    img: Optional[ObjectId]

    def __init__(self, oid: ObjectId, full_name: str, email: str, img: Optional[ObjectId]) -> None:
        super().__init__(oid)
        self.full_name = str(full_name)
        self.email = str(email)
        if img is not None:
            self.img = ObjectId(img)
        else:
            self.img = None

    def to_json(self) -> json:
        return {
            "_id": self.oid,
            "full_name": self.full_name,
            "email": self.email,
            "img": self.img,
        }

    @staticmethod
    def from_json(doc: json) -> User:
        return User(
            oid=ObjectId(doc["_id"]),
            full_name=doc["full_name"],
            email=doc["email"],
            img=doc["img"],
        )

    def __repr__(self) -> str:
        return f"User ID: {self.oid.__str__()}"
