import ttkbootstrap as tb
import tkinter as tk  # Import tkinter as tk

class SubTab2(tb.Frame):  # Inherit from tb.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Initialize as a Frame
        self.parent = parent

        # Create a notebook for horizontal sub-tabs
        notebook = tb.Notebook(self, bootstyle="default")  # Use self instead of parent
        notebook.pack(fill=tk.BOTH, expand=True)

        # Add Sub Tab 2.1
        frame1 = tb.Frame(notebook)
        notebook.add(frame1, text="Sub Tab 2.1")

        # Add content to Sub Tab 2.1
        label1 = tb.Label(frame1, text="Ni idea que hacer aca aun", font=('Arial', 14), bootstyle="inverse-light")
        label1.pack(expand=True, pady=20)

        # Add a button to Sub Tab 2.1
        button1 = tb.Button(frame1, text="Click Me", bootstyle="success", command=self.on_button_click_1)
        button1.pack(pady=10)

        # Add Sub Tab 2.2
        frame2 = tb.Frame(notebook)
        notebook.add(frame2, text="Sub Tab 2.2")

        # Add content to Sub Tab 2.2
        label2 = tb.Label(frame2, text="Ni idea que hacer aca aun", font=('Arial', 14), bootstyle="inverse-light")
        label2.pack(expand=True, pady=20)

        # Add an entry widget to Sub Tab 2.2
        self.entry = tb.Entry(frame2, bootstyle="primary", width=30)
        self.entry.pack(pady=10)

        # Add a button to Sub Tab 2.2
        button2 = tb.Button(frame2, text="Submit", bootstyle="info", command=self.on_button_click_2)
        button2.pack(pady=10)

    def on_button_click_1(self):
        print("Button in Sub Tab 2.1 clicked!")

    def on_button_click_2(self):
        user_input = self.entry.get()
        print(f"User entered: {user_input}")
