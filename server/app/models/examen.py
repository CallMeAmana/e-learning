from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .. import mongo

class Examen:
    def __init__(self, title, date, duration, _id=None):
        self.id = _id
        self.title = title
        self.date = date
        self.duration = duration

    def save(self):
        result = mongo.db.examen.insert_one({
            "title": self.title,
            "date": self.date,
            "duration": self.duration
        })
        self.id = result.inserted_id

    @staticmethod
    def get_by_id(examen_id):
        data = mongo.db.examen.find_one({"_id": ObjectId(examen_id)})
        if data:
            return Examen(title=data['title'], date=data['date'], duration=data['duration'], _id=data['_id'])
        return None

    def update(self, title, date, duration):
        mongo.db.examen.update_one(
            {"_id": ObjectId(self.id)},
            {"$set": {"title": title, "date": date, "duration": duration}}
        )

    def delete(self):
        mongo.db.examen.delete_one({"_id": ObjectId(self.id)})

    @staticmethod
    def get_all():
        examens = mongo.db.examen.find()
        return [Examen(title=ex['title'], date=ex['date'], duration=ex['duration'], _id=ex['_id']) for ex in examens]

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "date": self.date,
            "duration": self.duration
        }
