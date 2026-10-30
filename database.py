import sqlite3

DB_NAME = "railway.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Trains Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trains (
            train_number TEXT PRIMARY KEY,
            train_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            seats_available INTEGER NOT NULL,
            fare REAL NOT NULL
        )
    ''')

    # Create Bookings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT NOT NULL,
            train_number TEXT NOT NULL,
            seat_number INTEGER NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (train_number) REFERENCES trains(train_number)
        )
    ''')

    # Seed Sample Trains if table is empty
    cursor.execute('SELECT COUNT(*) FROM trains')
    if cursor.fetchone()[0] == 0:
        sample_trains = [
            ("12675", "Kovai Superfast Express", "Chennai Central", "Coimbatore Jn", 120, 240.0),
            ("12083", "Jan Shatabdi Express", "Mayiladuthurai", "Coimbatore Jn", 95, 180.0),
            ("16614", "Rajkot Express", "Coimbatore Jn", "Rajkot", 60, 850.0),
            ("20644", "Vande Bharat Express", "Coimbatore Jn", "Chennai Central", 80, 1365.0)
        ]
        cursor.executemany('''
            INSERT INTO trains (train_number, train_name, source, destination, seats_available, fare)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_trains)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")