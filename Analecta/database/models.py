from db_manager import DatabaseManager

db = DatabaseManager()

# Create Books Table
db.execute_query("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        status TEXT DEFAULT 'Not Started'
    )
""")

# Create Reading Log Table
db.execute_query("""
    CREATE TABLE IF NOT EXISTS reading_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        comments TEXT,
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
""")

db.close()
