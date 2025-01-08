# Python Imports
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


# Get DB From Cluster
_cluster: MongoClient = MongoClient(os.environ.get("DB_URI"))
PhoneBuddyDB: Database = _cluster["phonebuddy"]


class PhoneBuddyDB:
    phones_coll: Collection = PhoneBuddyDB.get_collection("phones")
    users_coll: Collection = PhoneBuddyDB.get_collection("users")
    files_coll: Collection = PhoneBuddyDB.get_collection("files")