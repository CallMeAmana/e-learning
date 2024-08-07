from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from .. import mongo 

class Admin:
    def __init__(self, nom, prenom, email, mdp):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        

    def save(self):
        last_admin = mongo.db.admin.find_one(sort=[("id", -1)])
        new_id = last_admin["id"] + 1 if last_admin and "id" in last_admin else 1
        admin_id = mongo.db.admin.insert_one({
            "id": new_id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mdp": self.mdp
        }).inserted_id
        return admin_id

    @staticmethod
    def get_by_id(admin_id):
        admin = mongo.db.admin.find_one({"id": admin_id})
        if admin:
            admin["_id"] = str(admin["_id"])  # Convert ObjectId to string
        return admin

    @staticmethod
    def get_all():
        return list(mongo.db.admin.find())

    @staticmethod
    def update(admin_id, data):
        if "_id" in data:
            del data["_id"]  # Remove _id from data to avoid modifying it
        updated_admin = mongo.db.admin.find_one_and_update(
            {"id": admin_id},
            {"$set": data},
            return_document=True
        )
        if updated_admin:
            updated_admin["_id"] = str(updated_admin["_id"])  # Convert ObjectId to string
        return updated_admin

    @staticmethod
    def delete(admin_id):
        return mongo.db.admin.delete_one({"id": admin_id})
