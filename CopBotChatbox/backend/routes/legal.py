from flask import Blueprint, jsonify
from backend.models.legal_section import LegalSection

legal_blueprint = Blueprint('legal', __name__)

@legal_blueprint.route('/sections', methods=['GET'])
def get_legal_sections():
    sections = LegalSection.query.all()
    result = [{'section_name': section.section_name, 'description': section.description} for section in sections]
    return jsonify(result), 200
