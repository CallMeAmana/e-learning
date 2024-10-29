from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .. import mongo

class Users:
    def __init__(self, nom, Role, modified, _id=None):
        self.id = _id
        self.nom = nom
        self.Role = modified
      
    @staticmethod
    def get_all():
        users = mongo.db.users.find()
        return [Users(nom=ex['nom'], Role=ex['Role'], modified=ex['modified'], _id=ex['_id']) for user in users]

    def to_dict(self):
        return {
            "id": str(self.id),
            "nom": self.nom,
            "Role": self.Role,
            "modified": self.modified
        }
