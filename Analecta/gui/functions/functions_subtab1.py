import ttkbootstrap as tb
import tkinter as tk
from tkinter import messagebox
from database.db_manager import DatabaseManager

class SubTab1:
    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseManager()

        # Create notebook
        notebook = tb.Notebook(parent, bootstyle="default")
        notebook.pack(fill=tk.BOTH, expand=True)

        # Frame for Sub Tab 1.1
        frame1 = tb.Frame(notebook)
        notebook.add(frame1, text="Library")

        # Treeview to display books
        self.tree = tb.Treeview(frame1, columns=("ID", "Title", "Author", "Genre", "Status"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Status", text="Status")

        # Populate the treeview
        self.populate_treeview()

        # Delete button
        delete_button = tb.Button(frame1, text="Delete Selected", bootstyle="danger", command=self.delete_book)
        delete_button.pack(pady=10)

    def populate_treeview(self):
        """Fetch books from the database and display them in the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        books = self.db.fetch_books()
        for book in books:
            self.tree.insert("", tk.END, values=book)

    def delete_book(self):
        """Delete the selected book from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a book to delete.")
            return

        book_id = self.tree.item(selected_item, "values")[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
        if confirm:
            self.db.delete_book(book_id)
            self.populate_treeview()

