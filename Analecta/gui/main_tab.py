import ttkbootstrap as tb
import tkinter as tk  
from gui.sub_tab_1 import SubTab1
from gui.sub_tab_2 import SubTab2
from gui.sub_tab_3 import SubTab3

class MainTab(tb.Frame):  # ✅ Inherit from tb.Frame to be packable
    def __init__(self, parent):
        super().__init__(parent)  # ✅ Proper inheritance
        self.pack(fill=tk.BOTH, expand=True)

        # Define custom names for each Main Tab
        self.tab_names = {
            1: "📚 Collection",
            2: "👓 Reading",
            3: "⭐ Wishlist"
        }

        # Vertical tab menu (left side)
        self.tab_menu = tb.Frame(self, width=150, bootstyle="dark")
        self.tab_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Main content area (right side)
        self.content_area = tb.Frame(self)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create main tabs and store their frames & sub-tabs
        self.main_tabs = {}
        self.main_tab_frames = {}
        self.sub_tabs = {}  # ✅ Store sub-tabs properly

        for i, name in self.tab_names.items():
            btn = tb.Button(self.tab_menu, text=name,  
                            command=lambda i=i: self.show_main_tab(i),
                            bootstyle="light-outline", width=15)
            btn.pack(fill=tk.X, pady=5, padx=5)
            self.main_tabs[i] = btn

            frame = tb.Frame(self.content_area)
            self.main_tab_frames[i] = frame

            # ✅ Correctly assign each sub-tab
            if i == 1:
                self.sub_tabs[i] = SubTab1(frame)
            elif i == 2:
                self.sub_tabs[i] = SubTab2(frame)
            elif i == 3:
                self.sub_tabs[i] = SubTab3(frame)

            self.sub_tabs[i].pack(fill=tk.BOTH, expand=True)  

        # 🚀 Footer Buttons (Exit, Config, Help)
        self.create_footer_buttons()

        # Show first main tab by default
        self.show_main_tab(1)

    def create_footer_buttons(self):
        """Creates footer buttons (Exit, Config, Help)."""
        self.footer_frame = tb.Frame(self.tab_menu)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Exit Button
        btn_exit = tb.Button(self.footer_frame, text="Exit", bootstyle="danger", 
                             command=self.quit_application)
        btn_exit.pack(side=tk.LEFT, padx=5)

        # Config Button (opens config window)
        btn_config = tb.Button(self.footer_frame, text="Config", bootstyle="info", 
                               command=self.open_config)
        btn_config.pack(side=tk.LEFT, padx=5)

        # Help ("?") Button (opens help window)
        btn_help = tb.Button(self.footer_frame, text="?", width=3, bootstyle="secondary", 
                             command=self.open_help)
        btn_help.pack(side=tk.LEFT, padx=5)

    def show_main_tab(self, tab_number):
        """Switches the main tab view."""
        for frame in self.main_tab_frames.values():
            frame.pack_forget()
        self.main_tab_frames[tab_number].pack(fill=tk.BOTH, expand=True)

        # Update button styles
        for btn in self.main_tabs.values():
            btn.configure(bootstyle="light-outline")
        self.main_tabs[tab_number].configure(bootstyle="primary")

    def quit_application(self):
        """Quits the main application safely."""
        root = self.winfo_toplevel()
        root.quit()

    def open_config(self):
        """Opens a modal config window centered on the main window."""
        self.open_modal("Configuration", "Configuration settings go here")

    def open_help(self):
        """Opens a modal help window centered on the main window."""
        self.open_modal("Help", "Help information goes here")

    def open_modal(self, title, message):
        """Reusable function to create modal windows."""
        modal_window = tk.Toplevel(self)
        modal_window.title(title)
        modal_window.geometry("300x200")
        modal_window.overrideredirect(True)  # Remove window bar
        modal_window.grab_set()  # Block main window until closed

        # Center the window
        self.center_window(modal_window, 300, 200)

        # Custom Close Button (Styled Like a Title Bar)
        close_frame = tb.Frame(modal_window, bootstyle="dark")
        close_frame.pack(fill=tk.X)
        btn_close = tb.Button(close_frame, text="❌", bootstyle="danger", 
                              command=modal_window.destroy, width=3)
        btn_close.pack(side=tk.RIGHT, padx=5, pady=2)

        tb.Label(modal_window, text=message).pack(pady=20)

        self.wait_window(modal_window)

    def center_window(self, window, width, height):
        """Centers a window relative to the root window."""
        
        # Find the actual root window (main Tkinter window)
        root = self.winfo_toplevel()  
        root.update_idletasks()

        # Get the root window's position and size
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_width = root.winfo_width()
        main_height = root.winfo_height()

        # Calculate centered position
        x = main_x + (main_width // 2) - (width // 2)
        y = main_y + (main_height // 2) - (height // 2)

        # Apply the new position
        window.geometry(f"{width}x{height}+{x}+{y}")
