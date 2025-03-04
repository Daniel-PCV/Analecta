import tkinter as tk
import ttkbootstrap as tb
from gui.main_tab import MainTab

class TabbedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analecta")

        # Remove default window bar
        self.root.overrideredirect(True)

        # Set window size
        WIDTH, HEIGHT = 1600, 1000
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.center_window(WIDTH, HEIGHT)

        # Custom Title Bar Frame
        self.title_bar = tb.Frame(root, bootstyle="#4e5d6c", padding=5)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        # Title Label
        self.title_label = tb.Label(self.title_bar, text="Analecta", font=("Arial", 12, "bold"), foreground="white")
        self.title_label.pack(side=tk.LEFT, padx=10)

        # Bind title bar events to allow dragging
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

        # Create main container
        self.main_frame = tb.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Initialize the main tab
        self.main_tab = MainTab(self.main_frame)

    def center_window(self, width, height):
        """Center the window on the screen."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def start_move(self, event):
        """Save initial mouse position when dragging starts."""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Move the window based on mouse movement."""
        x_offset = event.x_root - self.x
        y_offset = event.y_root - self.y
        self.root.geometry(f"+{x_offset}+{y_offset}")

if __name__ == "__main__":
    root = tb.Window(themename="superhero")  # Set the theme
    app = TabbedGUI(root)
    root.mainloop()
