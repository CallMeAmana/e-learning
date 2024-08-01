from flask import Blueprint, request, jsonify
from ..models.admin import Admin

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    admin = Admin(nom=data.get('nom'), prenom=data.get('prenom'), email=data.get('email'), mdp=data.get('mdp'))
    admin_id = admin.save()
    return jsonify({"id": str(admin_id)}), 201

@admin_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    admin = Admin.get_by_id(admin_id)
    if admin:
        return jsonify(admin), 200
    return jsonify({"error": "Admin not found"}), 404
    

@admin_bp.route('/admin/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    data = request.get_json()
    updated_admin = Admin.update(admin_id, data)
    if updated_admin:
        updated_admin["_id"] = str(updated_admin["_id"])  # Convert ObjectId to string
        return jsonify(updated_admin), 200
    return jsonify({"error": "Admin not found"}), 404


@admin_bp.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    result = Admin.delete(admin_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Admin deleted"}), 200
    return jsonify({"error": "Admin not found"}), 404

