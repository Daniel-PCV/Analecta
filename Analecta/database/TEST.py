import sqlite3
import config
# Connect to (or create) the database
db_path = "database/books.db" # Ensure this matches your actual DB path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the books table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER,
        genre_id INTEGER,
        rating INTEGER,
        language TEXT,
        format TEXT,
        isbn TEXT,
        pages INTEGER,
        date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_updated DATETIME,
        status TEXT CHECK(status IN ('Not Started', 'Reading', 'Completed')) DEFAULT 'Not Started',
        loan_status TEXT CHECK(loan_status IN ('Available', 'Borrowed')) DEFAULT 'Available',
        notes TEXT
    );
""")

# Commit and close
conn.commit()
conn.close()

print("Books table created successfully!")
