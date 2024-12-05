from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

DATABASE = os.getenv("DATABASE")
SECRET_KEY = os.getenv('SECRET_KEY')
USERS_SERVICE_URL = os.getenv('USERS_SERVICE_URL')

app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

@app.route('/vehicles', methods=['POST'])
@jwt_required() 
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
            brand:
              type: string
            model:
              type: string
            year:
              type: integer
            fuel_type:
              type: string
            purchase_price:
              type: number
            purchase_date:
              type: string
              format: date
            mileage_km:
              type: integer
            availability:
              type: string
              enum: ['Available', 'Not Available']
    responses:
      201:
        description: Vehicle successfully added.
      400:
        description: Missing required fields.
    """
    data = request.get_json()
    required_fields = ["brand", "model", "year", "fuel_type", "purchase_price", "purchase_date", "mileage_km", "availability"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute("""
        INSERT INTO vehicles (brand, model, year, fuel_type, purchase_price, purchase_date, mileage_km, availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data["brand"], data["model"], data["year"], data["fuel_type"], data["purchase_price"],
          data["purchase_date"], data["mileage_km"], data["availability"]))
    conn.commit()
    vehicle_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": vehicle_id, "message": "Vehicle added successfully"}), 201

@app.route('/vehicles', methods=['GET'])
@jwt_required()
def get_vehicles():
    """
    Retrieve vehicle details with optional filters.

    ---
    tags:
      - Vehicles
    parameters:
      - name: brand
        in: query
        type: string
        required: false
        description: Filter by vehicle brand.
      - name: model
        in: query
        type: string
        required: false
        description: Filter by vehicle model.
      - name: year
        in: query
        type: integer
        required: false
        description: Filter by vehicle year.
      - name: fuel_type
        in: query
        type: string
        required: false
        description: Filter by fuel type (e.g., 'Petrol', 'Diesel').
      - name: availability
        in: query
        type: string
        enum: ['Available', 'Not Available']
        required: false
        description: Filter by vehicle availability.
      - name: min_price
        in: query
        type: number
        required: false
        description: Filter by minimum purchase price.
      - name: max_price
        in: query
        type: number
        required: false
        description: Filter by maximum purchase price.
      - name: max_mileage
        in: query
        type: integer
        required: false
        description: Filter by maximum mileage (km).
    responses:
      200:
        description: List of vehicles.
    """
    filters = []
    query = "SELECT * FROM vehicles WHERE 1=1"

    # Filter by brand
    brand = request.args.get('brand')
    if brand:
        query += " AND brand = ?"
        filters.append(brand)

    # Filter by model
    model = request.args.get('model')
    if model:
        query += " AND model = ?"
        filters.append(model)

    # Filter by year
    year = request.args.get('year')
    if year:
        query += " AND year = ?"
        filters.append(year)

    # Filter by fuel type
    fuel_type = request.args.get('fuel_type')
    if fuel_type:
        query += " AND fuel_type = ?"
        filters.append(fuel_type)

    # Filter by availability
    availability = request.args.get('availability')
    if availability:
        query += " AND availability = ?"
        filters.append(availability)

    # Filter by price range
    min_price = request.args.get('min_price')
    if min_price:
        query += " AND purchase_price >= ?"
        filters.append(min_price)

    max_price = request.args.get('max_price')
    if max_price:
        query += " AND purchase_price <= ?"
        filters.append(max_price)

    # Filter by mileage
    max_mileage = request.args.get('max_mileage')
    if max_mileage:
        query += " AND mileage_km <= ?"
        filters.append(max_mileage)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query, filters)
    vehicles = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(vehicles), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
@jwt_required() 
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
            brand:
              type: string
            model:
              type: string
            year:
              type: integer
            fuel_type:
              type: string
            purchase_price:
              type: number
            purchase_date:
              type: string
              format: date
            mileage_km:
              type: integer
            availability:
              type: string
              enum: ['Available', 'Not Available']
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

    for key in ["brand", "model", "year", "fuel_type", "purchase_price", "purchase_date", "mileage_km", "availability"]:
        if key in data:
            updates.append(f"{key} = ?")
            params.append(data[key])
    
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    
    query = f"UPDATE vehicles SET {', '.join(updates)} WHERE vehicle_id = ?"
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
@jwt_required() 
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
    cursor = conn.execute("DELETE FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
    conn.commit()
    row_count = cursor.rowcount
    conn.close()
    
    if row_count == 0:
        return jsonify({"error": "Vehicle not found"}), 404
    
    return jsonify({"message": "Vehicle deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
