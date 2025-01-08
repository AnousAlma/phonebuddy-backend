"""
Item Model
"""

from __future__ import annotations
import json
from models.abstract_db_model import DB_MODEL
from bson import ObjectId

class Phone(DB_MODEL):
    oid: ObjectId
    brand: str
    phone: str
    monthly: str
    upfront: str
    image: str
    provider: str
    link: str

    def __init__(self, oid: ObjectId, brand: str, phone: str, monthly: str, upfront: str, image: str, provider: str, link: str) -> None:
        super().__init__(oid)
        self.brand = brand
        self.phone = phone
        self.monthly = monthly
        self.upfront = upfront
        self.image = image
        self.provider = provider
        self.link = link

    def to_json(self) -> json:
        return {
            "_id": self.oid,
            "brand": self.brand,
            "phone": self.phone,
            "monthly": self.monthly,
            "upfront": self.upfront,
            "image": self.image,
            "provider": self.provider,
            "link": self.link
        }

    @staticmethod
    def from_json(doc: json) -> Phone:
        return Phone(
            doc["_id"],
            doc["brand"],
            doc["phone"],
            doc["monthly"],
            doc["upfront"],
            doc["image"],
            doc["provider"],
            doc["link"]
        )

    def __repr__(self) -> str:
        return f"Phone ID: {self.oid.__str__()}, phone: {self.phone}"
