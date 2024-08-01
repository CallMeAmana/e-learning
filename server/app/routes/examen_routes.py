from flask import Blueprint, request, jsonify
from ..models.examen import Examen

examen_bp = Blueprint('examen', __name__)

@examen_bp.route('/examen', methods=['POST'])
def create_examen():
    data = request.get_json()
    title = data.get('title')
    date = data.get('date')
    duration = data.get('duration')
    examen = Examen(title=title, date=date, duration=duration)
    examen.save()
    return jsonify({"id": str(examen.id)}), 201

@examen_bp.route('/examen/<examen_id>', methods=['PUT'])
def update_examen(examen_id):
    data = request.get_json()
    title = data.get('title')
    date = data.get('date')
    duration = data.get('duration')
    examen = Examen.get_by_id(examen_id)
    if examen:
        examen.update(title=title, date=date, duration=duration)
        return jsonify({"message": "Examen updated successfully"}), 200
    return jsonify({"error": "Examen not found"}), 404

@examen_bp.route('/examen/<examen_id>', methods=['DELETE'])
def delete_examen(examen_id):
    examen = Examen.get_by_id(examen_id)
    if examen:
        examen.delete()
        return jsonify({"message": "Examen deleted successfully"}), 200
    return jsonify({"error": "Examen not found"}), 404

@examen_bp.route('/examens', methods=['GET'])
def get_all_examens():
    examens = Examen.get_all()
    return jsonify([examen.to_dict() for examen in examens]), 200

@examen_bp.route('/examen/<examen_id>', methods=['GET'])
def get_examen_by_id(examen_id):
    examen = Examen.get_by_id(examen_id)
    if examen:
        return jsonify(examen.to_dict()), 200
    return jsonify({"error": "Examen not found"}), 404
