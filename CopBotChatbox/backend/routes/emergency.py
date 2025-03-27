from flask import Blueprint, jsonify
from backend.models.emergency import EmergencyContact

emergency_blueprint = Blueprint('emergency', __name__)

@emergency_blueprint.route('/contacts', methods=['GET'])
def get_emergency_contacts():
    contacts = EmergencyContact.query.all()
    result = [{'name': contact.name, 'phone': contact.phone, 'description': contact.description} for contact in contacts]
    return jsonify(result), 200
