import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
# DATABASE = os.getenv("DATABASE")

def init_db():
    """Initializes the database and populates it with sample data."""
    conn = sqlite3.connect("damages.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS damages (
        damage_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        date TEXT NOT NULL,
        damage_severity TEXT CHECK(damage_severity IN ('Light', 'Moderate', 'Heavy')) NOT NULL,
        repair_status INTEGER NOT NULL
        
    );
    """)
    
    sample_data = [
        (3, "Fender bender", "2024-04-21", "Light", 1),
        (22, "Major crash - rearended", "2024-10-30", "Heavy", 0),
        (16, "Broken right tail light", "2024-09-12", "Light", 1),
        (54, "T-boned - passenger side", "2024-12-01", "Moderate", 0)
    ]
    
    cursor.executemany("""
    INSERT INTO damages (vehicle_id, description, date, damage_severity, repair_status)
    VALUES (?, ?, ?, ?, ?)
    """, sample_data)
    
    conn.commit()
    conn.close()
    print("Database initialized and sample data added.")

if __name__ == "__main__":
    init_db()
