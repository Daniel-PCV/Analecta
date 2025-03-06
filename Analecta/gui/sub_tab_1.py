import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from database.db_manager import DatabaseManager

class SubTab1(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.collection_tab = ttk.Frame(self)
        self.add_book_tab = ttk.Frame(self)

        self.add(self.collection_tab, text="📚 My Collection")
        self.add(self.add_book_tab, text="➕ Add Book")

        self.create_collection_view()
        self.create_add_book_view()

        self.selected_book_id = None  
        self.pack(fill=tk.BOTH, expand=True)

    #   FUNCTION : Add Books to DB  

    def add_book(self):
        title = self.entries["Title"].get()
        author = self.entries["Author"].get()
        genre = self.entries["Genre"].get()
        language = self.entries["Language"].get()
        book_format = self.entries["Format"].get()
        rating = self.entries["Rating"].get()
        isbn = self.entries["ISBN"].get()
        pages = self.entries["Pages"].get()
        notes = self.entries["Notes"].get()

        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required!")
            return

        try:
            pages = int(pages) if pages else None
        except ValueError:
            messagebox.showerror("Error", "Pages must be a number!")
            return

        author_id = self.db.get_or_create_author(author)
        genre_id = self.db.get_or_create_genre(genre)

        self.db.insert_book(title, author_id, genre_id, rating, language, book_format, isbn, pages, notes)
        self.populate_treeview()
        messagebox.showinfo("Success", "Book added successfully!")
        self.clear_fields()
        

    #   FUNCTION : Clears all fields on Add Books form

    def clear_fields(self):
        """Clears all input fields in the add book form."""
        for field in self.entries.values():
            if isinstance(field, ttk.Combobox):
                field.set("")
            else:
                field.delete(0, tk.END)
        
        self.selected_book_id = None
        self.add_button.config(state=tk.NORMAL)
        self.update_button.config(state=tk.DISABLED)


    def update_book(self):
        if not self.selected_book_id:
            messagebox.showerror("Error", "No book selected for update!")
            return

        title = self.entries["Title"].get()
        author = self.entries["Author"].get()
        genre = self.entries["Genre"].get()
        rating = self.entries["Rating"].get()

        if not title or not author:
            messagebox.showerror("Error", "Title and Author are required!")
            return

        author_id = self.db.get_or_create_author(author)
        genre_id = self.db.get_or_create_genre(genre)

        self.db.update_book(self.selected_book_id, title, author_id, genre_id, rating)
        self.populate_treeview(keep_selection=True)
        messagebox.showinfo("Success", "Book updated successfully!")
        self.clear_fields()

    def create_collection_view(self):
        self.collection_frame = ttk.Frame(self.collection_tab)
        self.collection_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            self.collection_frame,
            columns=("ID", "Title", "Author", "Genre", "Rating"),
            show="headings"
        )
        for col in ("ID", "Title", "Author", "Genre", "Rating"):
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.load_selected_book)

        self.button_frame = ttk.Frame(self.collection_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.delete_button = tb.Button(
            self.button_frame, text="🗑️ Delete Book", bootstyle="danger", command=self.delete_book
        )
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.populate_treeview()

    def populate_treeview(self, keep_selection=False):
        selected_item = self.tree.selection()
        selected_book_id = None
        if selected_item:
            selected_book_id = self.tree.item(selected_item, "values")[0]

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        books = self.db.fetch_books()
        for book in books:
            self.tree.insert("", tk.END, values=book)
        
        if keep_selection and selected_book_id:
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[0] == selected_book_id:
                    self.tree.selection_set(item)
                    break

    def delete_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to delete!")
            return

        book_id = self.tree.item(selected_item, "values")[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            self.db.delete_book(book_id)
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.clear_fields()

    def load_selected_book(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        book_data = self.tree.item(selected_item, "values")
        if not book_data:
            return

        self.selected_book_id = book_data[0]
        self.entries["Title"].delete(0, tk.END)
        self.entries["Title"].insert(0, book_data[1])
        self.entries["Author"].set(book_data[2])
        self.entries["Genre"].set(book_data[3])
        self.entries["Rating"].set(book_data[4])
        
        self.add_button.config(state=tk.DISABLED)
        self.update_button.config(state=tk.NORMAL)

    def create_add_book_view(self):
        self.frame1 = ttk.Frame(self.add_book_tab)
        self.frame1.pack(fill=tk.X, padx=10, pady=5)
        
        self.entries = {}
        fields = ["Title", "ISBN", "Pages", "Notes"]
        dropdown_fields = {
            "Author": self.db.fetch_authors(),
            "Genre": self.db.fetch_genres(),
            "Language": ["English", "Spanish", "French", "German"],  # Add Language here #pending 
            "Format": ["Hardcover", "Paperback", "Ebook", "Audiobook"],
            "Rating": list(range(1, 11))
        }

        
        for i, field in enumerate(fields):
            label = ttk.Label(self.frame1, text=field)
            label.grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            entry = ttk.Entry(self.frame1)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.W)
            self.entries[field] = entry
        
        row_offset = len(fields)
        for i, (field, values) in enumerate(dropdown_fields.items()):
            label = ttk.Label(self.frame1, text=field)
            label.grid(row=row_offset + i, column=0, padx=5, pady=2, sticky=tk.W)
            combo = ttk.Combobox(self.frame1, values=values, state="readonly")
            combo.grid(row=row_offset + i, column=1, padx=5, pady=2, sticky=tk.W)
            self.entries[field] = combo
        
        self.button_frame = ttk.Frame(self.frame1)
        self.button_frame.grid(row=row_offset + len(dropdown_fields), column=0, columnspan=2, pady=10)
        
        self.add_button = tb.Button(self.button_frame, text="📥 Add Book", bootstyle="primary", command=self.add_book)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.update_button = tb.Button(self.button_frame, text="✏️ Update Book", bootstyle="warning", state=tk.DISABLED, command=self.update_book)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tb.Button(self.button_frame, text="🧹 Clear Fields", bootstyle="secondary", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)



