# Damage Service API

This API allows the user to sort and manage through damages that have come upon their cars, with all CRUD-operations present.

## Features
- **Add Damages**: Add a new damage to the existing database.
- **Get Damages**: Retrieve a list of damages with relevant filters.
- **Update Damages**: Update details of a damage by ID.
- **Delete Damages**: Delete a damage by ID.
- **Endpoints**: View all available API endpoints with descriptions and methods.

## Setup

### Requirements
- Python 3.8+
- Flask
- SQLite3
- Flasgger (for Swagger UI)
- Flask-JWT-Extended
- python-dotenv

### Installing and running the code

1. Clone the repository:

   ```bash
   git clone https://github.com/jlkansakar/damage-service
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

Once the server is up and running, you can access the API documentation here:

```
http://127.0.0.1:5000/apidocs/
```

### Authentication

This application uses JWT (JSON Web Tokens) for authentication. You must include a valid JWT token in the `Authorization` header for all secure endpoints. The token should formatted in the following way:

```
Authorization: Bearer <your_jwt_token>
```

### Endpoints

1. **POST /add**
   - Add a new damage instance.
   - Requires JWT token.

2. **GET /list**
   - Retrieve damage details with optional query filters.
   - Requires JWT token.

3. **PUT /update**
   - Update damage details by ID.
   - Requires JWT token.

4. **DELETE /remove**
   - Delete a damage by ID.
   - Requires JWT token.

5. **GET /**
   - List all available API endpoints with their descriptions, methods, and JWT requirements.
   - No authentication required.

## Example Usage

### Add damage
```bash
curl -X POST http://127.0.0.1:5000/add \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{
   "vehicle_id": 27,
   "description": "Right turn crash - front fender right side is crushed",
   "date": "2024-07-06,
   "damage_severity": "Moderate",
   "repair_status": 1
}'
```

### Get Damages
```bash
curl -X GET "http://127.0.0.1:5000/list" \
-H "Authorization: Bearer <your_jwt_token>"
```

### Update damage 
```bash
curl -X PUT "http://127.0.0.1:5000/update/1" \
-H "Authorization: Bearer <your_jwt_token>" \
-H "Content-Type: application/json" \
-d '{
  "repair_status": 1
}'
```

### Delete damage
```bash
curl -X DELETE "http://127.0.0.1:5000/remove/1" \
-H "Authorization: Bearer <your_jwt_token>"
```
