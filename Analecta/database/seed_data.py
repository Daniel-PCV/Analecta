from db_manager import DatabaseManager

db = DatabaseManager()

# Insert sample books
books = [
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", "Completed"),
    ("1984", "George Orwell", "Dystopian", "Reading"),
    ("To Kill a Mockingbird", "Harper Lee", "Classic", "Not Started")
]

for book in books:
    db.execute_query("INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, ?)", book)

db.close()
print("Sample data added successfully!")
