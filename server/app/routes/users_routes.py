from flask import Blueprint, jsonify, request
from app import mongo
from bson.objectid import ObjectId


users_bp = Blueprint('users', __name__)
from datetime import datetime, timedelta

@users_bp.route('/users/<user_id>/ban', methods=['PUT'])
def ban_user(user_id):
    try:
        # Fetch ban duration from the request body
        data = request.json
        ban_duration = data.get("banDuration", None)  # Get the ban duration

        if ban_duration is None:
            return jsonify({"error": "Ban duration is required"}), 400

        # Ensure ban_duration is a positive integer
        if not isinstance(ban_duration, int) or ban_duration <= 0:
            return jsonify({"error": "Ban duration must be a positive integer"}), 400

        # Calculate ban start and end dates
        banStartDate = datetime.utcnow()
        banEndDate = banStartDate + timedelta(days=ban_duration)
        
        # Update the user's status to 'banned' with the calculated ban dates
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "status": "banned",
                "banStartDate": banStartDate.isoformat(),
                "banEndDate": banEndDate.isoformat()
            }}
        )

        if result.matched_count:
            return jsonify({"message": "User banned successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print(f"Error banning user: {e}")  # Log the error in the terminal
        return jsonify({"error": "An error occurred while banning the user"}), 500


# Exécutez la fonction check_ban_status périodiquement (tâche de fond ou cron job nécessaire)
def check_ban_status():
    current_date = datetime.utcnow()

    # Trouver tous les utilisateurs dont la date de fin de bannissement est passée
    users_to_unban = mongo.db.users.find({"status": "banned", "banEndDate": {"$lte": current_date}})
    
    for user in users_to_unban:
        # Rétablir l'utilisateur à l'état 'accepted' et supprimer les champs 'banEndDate' et 'banStartDate'
        mongo.db.users.update_one(
            {"_id": user['_id']},
            {"$set": {"status": "accepted"}, "$unset": {"banEndDate": "", "banStartDate": ""}}
        )

# Autres routes non modifiées
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    user_list = []
    for user in users:
        user_list.append({
            "id": str(user['_id']),
            "nom": user['nom'],
            "prenom": user['prenom'],
            "Role": user['Role'],
            "modified": user['modified'],
            "email": user['email'],
            "status": user.get('status', 'new'),
            "banStartDate": user.get('banStartDate'),
            "banEndDate": user.get('banEndDate')  # Ajouter la date de fin de bannissement si disponible
        })
    return jsonify(user_list)

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user_data = {
            "id": str(user['_id']),
            "nom": user['nom'],
            "prenom": user['prenom'],
            "Role": user['Role'],
            "modified": user['modified'],
            "email": user['email'],
            "status": user.get('status', 'new'),
            "banEndDate": user.get('banEndDate')  # Ajouter la date de fin de bannissement si disponible
        }
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    # Extract fields to update
    update_fields = {
        "nom": data.get('nom'),
        "prenom": data.get('prenom'),
        "Role": data.get('Role'),
        "email": data.get('email'),
        "motDePasse": data.get('motDePasse'),
        "status": data.get('status', 'new')  # Default status is 'new' if not set
    }

    # Remove any fields that are not provided in the request
    update_fields = {k: v for k, v in update_fields.items() if v is not None}

    # Update the user document
    result = mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully"}), 200

@users_bp.route('/users/status/<status>', methods=['GET'])
def get_users_by_status(status):
    users = mongo.db.users.find({"status": status})
    user_list = []
    for user in users:
        user_list.append({
            "id": str(user['_id']),
            "nom": user['nom'],
            "prenom": user['prenom'],
            "Role": user['Role'],
            "modified": user['modified'],
            "email": user['email'],
            "status": user.get('status', 'new')  # Default status is 'new' if not set
        })
    return jsonify(user_list)




@users_bp.route('/users/accepted/professors', methods=['GET'])
def get_accepted_professors_count():
    count = mongo.db.users.count_documents({"status": "accepted", "Role": "Professor"})
    return jsonify({"count": count})

@users_bp.route('/users/accepted/students', methods=['GET'])
def get_accepted_students_count():
    count = mongo.db.users.count_documents({"status": "accepted", "Role": "Student"})
    return jsonify({"count": count})

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200
