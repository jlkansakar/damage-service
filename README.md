# Vehicle Service API

This API allows users to manage vehicle data in a database, including adding, retrieving, updating, and deleting vehicles. It supports JWT authentication for secure access.

## Features
- **Add Vehicle**: Add a new vehicle to the database.
- **Get Vehicles**: Retrieve a list of vehicles with optional filters (e.g., brand, model, year, price).
- **Update Vehicle**: Update details of a vehicle by ID.
- **Delete Vehicle**: Delete a vehicle by ID.
- **Endpoints**: View all available API endpoints with descriptions and methods.

## Setup

### Requirements
- Python 3.8+
- Flask
- SQLite3
- Flasgger (for Swagger UI)
- Flask-JWT-Extended
- python-dotenv

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Fred062f/vehicle-service.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and set the following environment variables:

   ```env
   DATABASE=path_to_your_database.db
   SECRET_KEY=your_jwt_secret_key
   ```

4. Initialize the database by running the `init_db()` function (this should set up the database tables).

   ```bash
   python app.py
   ```

### Running the Application

To run the API:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

### API Documentation

Once the server is running, you can access the API documentation at:

```
http://127.0.0.1:5000/apidocs/
```

### Authentication

This API uses JWT (JSON Web Tokens) for authentication. You must include a valid JWT token in the `Authorization` header for all secure endpoints. The token should be in the format:

```
Authorization: Bearer <your_jwt_token>
```

### Endpoints

1. **POST /vehicles**
   - Add a new vehicle.
   - Requires JWT token.

2. **GET /vehicles**
   - Retrieve vehicle details with optional query filters.
   - Requires JWT token.

3. **PUT /vehicles/{vehicle_id}**
   - Update vehicle details by ID.
   - Requires JWT token.

4. **DELETE /vehicles/{vehicle_id}**
   - Delete a vehicle by ID.
   - Requires JWT token.

5. **GET /endpoints**
   - List all available API endpoints with their descriptions, methods, and JWT requirements.
   - No authentication required.

## Example Usage

### Add Vehicle
```bash
curl -X POST http://127.0.0.1:5000/vehicles \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "fuel_type": "Petrol",
  "purchase_price": 20000,
  "purchase_date": "2020-01-01",
  "mileage_km": 15000,
  "availability": "Available"
}'
```

### Get Vehicles
```bash
curl -X GET "http://127.0.0.1:5000/vehicles?brand=Toyota&availability=Available" \
-H "Authorization: Bearer <your_jwt_token>"
```

### Update Vehicle
```bash
curl -X PUT "http://127.0.0.1:5000/vehicles/1" \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{
  "availability": "Not Available"
}'
```

### Delete Vehicle
```bash
curl -X DELETE "http://127.0.0.1:5000/vehicles/1" \
-H "Authorization: Bearer <your_jwt_token>"
```
