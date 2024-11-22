from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)
DATABASE = os.getenv("DATABASE")

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    """
    Add a new vehicle to the database.
    
    ---
    tags:
      - Vehicles
    parameters:
      - name: body
        in: body
        required: true
        description: Vehicle details
        schema:
          type: object
          properties:
            make:
              type: string
            model:
              type: string
            year:
              type: integer
            price:
              type: number
            availability:
              type: boolean
    responses:
      201:
        description: Vehicle successfully added.
      400:
        description: Missing required fields.
    """
    data = request.get_json()
    required_fields = ["make", "model", "year", "price"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("""
        INSERT INTO vehicles (make, model, year, price, availability)
        VALUES (?, ?, ?, ?, ?)
    """, (data["make"], data["model"], data["year"], data["price"], data.get("availability", True)))
    conn.commit()
    vehicle_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": vehicle_id, "message": "Vehicle added successfully"}), 201

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    """
    Retrieve vehicle details with optional filters.
    
    ---
    tags:
      - Vehicles
    parameters:
      - name: make
        in: query
        type: string
        required: false
        description: Filter by vehicle make.
      - name: model
        in: query
        type: string
        required: false
        description: Filter by vehicle model.
    responses:
      200:
        description: List of vehicles.
    """
    filters = []
    query = "SELECT * FROM vehicles WHERE 1=1"
    
    make = request.args.get('make')
    if make:
        query += " AND make = ?"
        filters.append(make)
    
    model = request.args.get('model')
    if model:
        query += " AND model = ?"
        filters.append(model)
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query, filters)
    vehicles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(vehicles), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """
    Update vehicle details by ID.
    
    ---
    tags:
      - Vehicles
    parameters:
      - name: vehicle_id
        in: path
        type: integer
        required: true
        description: ID of the vehicle to update.
      - name: body
        in: body
        required: true
        description: Updated vehicle details.
        schema:
          type: object
          properties:
            make:
              type: string
            model:
              type: string
            year:
              type: integer
            price:
              type: number
            availability:
              type: boolean
    responses:
      200:
        description: Vehicle successfully updated.
      404:
        description: Vehicle not found.
      400:
        description: No fields to update.
    """
    data = request.get_json()
    updates = []
    params = []

    for key in ["make", "model", "year", "price", "availability"]:
        if key in data:
            updates.append(f"{key} = ?")
            params.append(data[key])
    
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    
    query = f"UPDATE vehicles SET {', '.join(updates)} WHERE id = ?"
    params.append(vehicle_id)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute(query, params)
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Vehicle not found"}), 404
    
    return jsonify({"message": "Vehicle updated successfully"}), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """
    Delete a vehicle by ID.
    
    ---
    tags:
      - Vehicles
    parameters:
      - name: vehicle_id
        in: path
        type: integer
        required: true
        description: ID of the vehicle to delete.
    responses:
      200:
        description: Vehicle successfully deleted.
      404:
        description: Vehicle not found.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Vehicle not found"}), 404
    
    return jsonify({"message": "Vehicle deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
