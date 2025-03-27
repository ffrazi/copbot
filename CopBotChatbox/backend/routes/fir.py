from flask import Blueprint, jsonify

fir_blueprint = Blueprint('fir', __name__)

@fir_blueprint.route('/guidelines', methods=['GET'])
def get_fir_guidelines():
    guidelines = "To file an FIR, follow these steps: ... (include your process here)"
    return jsonify({'guidelines': guidelines}), 200
