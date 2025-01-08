"""
Location Model
"""

from __future__ import annotations
import json
from models.abstract_db_model import DB_MODEL
from bson import ObjectId, binary


class MongoDBfile(DB_MODEL):
    oid: ObjectId
    file_type: str  # .png | .pdf | etc
    file_bytes: binary

    def __init__(self, oid: ObjectId, file_type: str, file_bytes: binary) -> None:
        super().__init__(oid)
        self.file_type = str(file_type)
        self.file_bytes = file_bytes

    def to_json(self) -> json:
        return {
            "_id": self.oid,
            "file_type": self.file_type,
            "file_bytes": self.file_bytes
        }

    @staticmethod
    def from_json(doc: json) -> MongoDBfile:
        return MongoDBfile(
            oid=ObjectId(doc["_id"]),
            file_type=doc["file_type"],
            file_bytes=doc["file_bytes"]
        )

    def __repr__(self) -> str:
        return f"File ID: {self.oid.__str__()}, File Type: {self.file_type}"

