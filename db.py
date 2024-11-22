import sqlite3

def init_db():
    """Initializes the database and populates it with sample data."""
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        price REAL NOT NULL,
        availability BOOLEAN NOT NULL DEFAULT 1
    );
    """)
    
    sample_data = [
        ("Toyota", "Corolla", 2020, 15000, True),
        ("Honda", "Civic", 2019, 16000, True),
        ("Ford", "Focus", 2021, 18000, True),
        ("BMW", "3 Series", 2018, 25000, False)
    ]
    cursor.executemany("""
    INSERT INTO vehicles (make, model, year, price, availability)
    VALUES (?, ?, ?, ?, ?)
    """, sample_data)
    
    conn.commit()
    conn.close()
    print("Database initialized and sample data added.")

if __name__ == "__main__":
    init_db()
