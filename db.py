import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")

def init_db():
    """Initializes the database and populates it with sample data."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        fuel_type TEXT NOT NULL,
        purchase_price REAL NOT NULL,
        purchase_date DATE NOT NULL,
        mileage_km INTEGER NOT NULL,
        availability TEXT CHECK(availability IN ('Available', 'Not Available')) NOT NULL
    );
    """)
    
    sample_data = [
        ("Toyota", "Corolla", 2020, "Petrol", 15000.00, "2020-05-15", 20000, "Available"),
        ("Honda", "Civic", 2019, "Diesel", 16000.00, "2019-03-10", 30000, "Available"),
        ("Ford", "Focus", 2021, "Hybrid", 18000.00, "2021-07-25", 15000, "Available"),
        ("BMW", "3 Series", 2018, "Petrol", 25000.00, "2018-10-20", 50000, "Not Available")
    ]
    
    cursor.executemany("""
    INSERT INTO vehicles (brand, model, year, fuel_type, purchase_price, purchase_date, mileage_km, availability)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_data)
    
    conn.commit()
    conn.close()
    print("Database initialized and sample data added.")

if __name__ == "__main__":
    init_db()
