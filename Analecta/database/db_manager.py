import sqlite3

class DatabaseManager:
    def __init__(self, db_name="database/books.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates necessary tables if they do not exist"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            genre_id INTEGER,
            rating INTEGER CHECK(rating BETWEEN 1 AND 10),
            language TEXT,
            format TEXT,
            isbn TEXT,
            pages INTEGER,
            status TEXT CHECK(status IN ('Not Started', 'Reading', 'Completed')) DEFAULT 'Not Started',
            loan_status TEXT CHECK(loan_status IN ('Available', 'Borrowed')) DEFAULT 'Available',
            notes TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        )
        """)

        self.conn.commit()

    def insert_book(self, title, author_id, genre_id, rating, language, book_format, isbn, pages, notes):
        """Inserts a new book into the database."""
        query = """
        INSERT INTO books (title, author_id, genre_id, rating, language, format, 
                           isbn, pages, status, loan_status, notes, date_added, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Not Started', 'Available', ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        params = (title, author_id, genre_id, rating, language, book_format, isbn, pages, notes)
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_books(self):
        """Retrieve book information with author and genre names."""
        query = """
        SELECT books.id, books.title, authors.name, genres.name, books.rating, books.language, 
               books.format, books.isbn, books.pages, books.status, books.loan_status, books.notes,
               books.date_added, books.last_updated
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
        LEFT JOIN genres ON books.genre_id = genres.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_book(self, book_id, title=None, author_id=None, genre_id=None, rating=None, 
                    language=None, book_format=None, isbn=None, pages=None, status=None, 
                    loan_status=None, notes=None):
        """Updates book details."""
        updates = []
        params = []

        if title:
            updates.append("title = ?")
            params.append(title)
        if author_id:
            updates.append("author_id = ?")
            params.append(author_id)
        if genre_id:
            updates.append("genre_id = ?")
            params.append(genre_id)
        if rating:
            updates.append("rating = ?")
            params.append(rating)
        if language:
            updates.append("language = ?")
            params.append(language)
        if book_format:
            updates.append("format = ?")
            params.append(book_format)
        if isbn:
            updates.append("isbn = ?")
            params.append(isbn)
        if pages:
            updates.append("pages = ?")
            params.append(pages)
        if status:
            updates.append("status = ?")
            params.append(status)
        if loan_status:
            updates.append("loan_status = ?")
            params.append(loan_status)
        if notes:
            updates.append("notes = ?")
            params.append(notes)

        if updates:
            updates.append("last_updated = CURRENT_TIMESTAMP")
            query = f"UPDATE books SET {', '.join(updates)} WHERE id = ?"
            params.append(book_id)
            self.cursor.execute(query, params)
            self.conn.commit()

    def delete_book(self, book_id):
        """Deletes a book by ID."""
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()

    def close(self):
        """Closes the database connection."""
        self.conn.close()

    def get_or_create_author(self, author_name):
        """Retrieve or insert an author and return their ID."""
        self.cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  
        
        self.cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        self.conn.commit()
        return self.cursor.lastrowid  
    
    def get_or_create_genre(self, genre_name):
        """Retrieve or insert a genre and return its ID."""
        self.cursor.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  

        self.cursor.execute("INSERT INTO genres (name) VALUES (?)", (genre_name,))
        self.conn.commit()
        return self.cursor.lastrowid  

    def fetch_authors(self):
        """Fetch all authors from the database."""
        self.cursor.execute("SELECT name FROM authors")
        return [row[0] for row in self.cursor.fetchall()]

    def fetch_genres(self):
        """Fetch all genres from the database."""
        self.cursor.execute("SELECT name FROM genres")
        return [row[0] for row in self.cursor.fetchall()]




