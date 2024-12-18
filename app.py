from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from db import init_db
import inspect


load_dotenv()

app = Flask(__name__)

DATABASE = os.getenv("DATABASE")
SECRET_KEY = os.getenv('SECRET_KEY')


app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token in the format **Bearer &lt;token&gt;**.",
        }
    },
    "security": [{"BearerAuth": []}],
}
swagger = Swagger(app, config=swagger_config)

init_db()

@app.route('/add', methods=['POST'])
@jwt_required() 
def add_damage():
    """
    Add a new damage to the database.
    
    ---
    tags:
      - Damages
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        description: Damage details
        schema:
          type: object
          properties:
            vehicle_id:
              type: string
            description:
              type: string
            date:
              type: string
            damage_severity:
              type: string
              enum: ['Light', 'Moderate', 'Heavy']
            repair_status:
              type: integer
    responses:
      201:
        description: Damage successfully added.
      400:
        description: Missing required fields.
    """
    data = request.get_json()
    required_fields = ["vehicle_id", "description", "date", "damage_severity", "repair_status"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("""
        INSERT INTO damages (vehicle_id, description, date, damage_severity, repair_status)
        VALUES (?, ?, ?, ?, ?)
    """, (data["vehicle_id"], data["description"], data["date"], data["damage_severity"], data["repair_status"]))
    conn.commit()
    damage_id = cursor.lastrowid
    conn.close()
    return jsonify({"damage_id": damage_id, "message": "Damage added successfully"}), 201

@app.route('/list', methods=['GET'])
@jwt_required()
def get_damages():
    """
    Retrieve damage details with optional filters.

    ---
    tags:
      - Damages
    security:
      - BearerAuth: []
    parameters:
      - name: damage_id
        in: query
        type: integer
        required: false
        description: Filter by damage id.
      - name: damage_severity
        in: query
        type: string
        enum: ['Light', 'Moderate', 'Heavy']
        required: false
        description: Filter by damage severity.
    responses:
      200:
        description: List of damages.
    """
    filters = []
    query = "SELECT * FROM damages WHERE 1=1"

    # Filter by damage_id
    damage_id = request.args.get('damage_id')
    if damage_id:
        query += " AND damage_id = ?"
        filters.append(damage_id)

    # Filter by damage severity
    damage_severity = request.args.get('damage_severity')
    if damage_severity:
        query += " AND damage_severity = ?"
        filters.append(damage_severity)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query, filters)
    vehicles = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(vehicles), 200


@app.route('/update/<int:damage_id>', methods=['PUT'])
@jwt_required() 
def update_damages(damage_id):
    """
    Update damage details by ID.
    
    ---
    tags:
      - Damages
    security:
      - BearerAuth: []
    parameters:
      - name: damage_id
        in: path
        type: integer
        required: true
        description: ID of the damage to update.
      - name: body
        in: body
        required: true
        description: Updated damage details.
        schema:
          type: object
          properties:
            vehicle_id:
              type: string
            description:
              type: string
            date:
              type: string
            damage_severity:
              type: string
              enum: ['Light', 'Moderate', 'Heavy']
            repair_status:
              type: integer
    responses:
      200:
        description: Damage successfully updated.
      404:
        description: Damage not found.
      400:
        description: No fields to update.
    """
    data = request.get_json()
    updates = []
    params = []

    for key in ["vehicle_id", "description", "date", "damage_severity", "repair_status"]:
        if key in data:
            updates.append(f"{key} = ?")
            params.append(data[key])
    
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    
    query = f"UPDATE damages SET {', '.join(updates)} WHERE damage_id = ?"
    params.append(damage_id)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute(query, params)
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Damage not found"}), 404
    
    return jsonify({"message": "Damage updated successfully"}), 200

@app.route('/remove/<int:damage_id>', methods=['DELETE'])
@jwt_required() 
def delete_damage(damage_id):
    """
    Delete a damage by ID.
    
    ---
    tags:
      - Damages
    security:
      - BearerAuth: []
    parameters:
      - name: damage_id
        in: path
        type: integer
        required: true
        description: ID of the damage to delete.
    responses:
      200:
        description: Damage successfully deleted.
      404:
        description: Damage not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("DELETE FROM damages WHERE damage_id = ?", (damage_id,))
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Damage not found"}), 404
    
    return jsonify({"message": "Damage deleted successfully"}), 200


@app.route('/', methods=['GET'])
def endpoints():
    """
    List all available endpoints in the API, including their descriptions, methods, and JWT token requirements.
    --- 
    tags:
      - Utility
    responses:
      200:
        description: A list of all available routes with their descriptions, methods, and JWT token requirements.
    """
    excluded_endpoints = {'static', 'flasgger.static', 'flasgger.oauth_redirect', 'flasgger.<lambda>', 'flasgger.apispec'}
    excluded_methods = {'HEAD', 'OPTIONS'}
    routes = []

    for rule in app.url_map.iter_rules():
        if rule.endpoint not in excluded_endpoints:
            func = app.view_functions.get(rule.endpoint)
            if not func:
                continue

            # Get the docstring
            full_docstring = inspect.getdoc(func)
            docstring = full_docstring.split('---')[0].replace("\n", " ").strip() if full_docstring else None

            # Check if the @jwt_required() decorator is applied
            jwt_required = "@jwt_required" in inspect.getsource(func).split('\n')[1]

            # Exclude methods
            methods = list(rule.methods - excluded_methods)

            routes.append({
                'endpoint': rule.rule,
                'methods': methods,
                'description': docstring,
                'jwt_required': jwt_required
            })
    return jsonify({'endpoints': routes}), 200




if __name__ == '__main__':
    app.run(debug=True)
