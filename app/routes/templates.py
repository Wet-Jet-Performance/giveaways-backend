from flask import Blueprint, request, jsonify
import os

templates_bp = Blueprint("templates", __name__, url_prefix="/templates")

@templates_bp.route('', methods=['GET', 'POST'])
def manage_template():
    # Get the absolute path to the 'app' directory
    app_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # Construct the path to the template file
    template_path = os.path.join(app_dir, 'templates', 'new_tickets_email.html')
    
    if request.method == 'GET':
        try:
            with open(template_path, 'r') as file:
                content = file.read()
            return jsonify({'content': content})
        except FileNotFoundError:
            return jsonify({'error': 'Template file not found'}), 404
    
    elif request.method == 'POST':
        new_content = request.json.get('content')
        if new_content:
            try:
                with open(template_path, 'w') as file:
                    file.write(new_content)
                return jsonify({'message': 'Template updated successfully'}), 200
            except IOError:
                return jsonify({'error': 'Failed to write to template file'}), 500
        else:
            return jsonify({'error': 'No content provided'}), 400