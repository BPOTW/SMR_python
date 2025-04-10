import tkinter as tk
import customtkinter as ctk
from ui.custom_functions import CustomFunctions

class BaseScreen(ctk.CTkFrame):
    """
    Base screen class that provides common functionality for all screens.
    All screens should inherit from this class.
    """
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.custom = CustomFunctions()
        
        # Configure grid layout for proper expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def show_message(self, title, message, message_type="info"):
        """Show a message dialog"""
        self.custom.show_message(title, message, message_type)
    
    def confirm_dialog(self, title, message):
        """Show a confirmation dialog"""
        return self.custom.confirm_dialog(title, message)
    
    def create_header(self, title):
        """Create a standard header with title"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(side="left")
        
        # Add current date on the right
        date_label = ctk.CTkLabel(
            header_frame,
            text=self.custom.format_date(),
            font=ctk.CTkFont(size=14)
        )
        date_label.pack(side="right")
        
        return header_frame
    
    def create_sidebar(self, buttons, default_selected=None):
        """
        Create a sidebar with navigation buttons
        
        Args:
            buttons: List of tuples (text, command)
            default_selected: The default selected button
        """
        # Create sidebar frame
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # App logo and title
        logo_label = ctk.CTkLabel(
            sidebar, 
            text="Smart Result System",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        logo_label.pack(pady=(20, 30), padx=20)
        
        # Create sidebar buttons
        sidebar_buttons = {}
        for text, command in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                fg_color="transparent",
                anchor="w",
                command=command,
                height=40
            )
            btn.pack(pady=5, padx=10, fill="x")
            sidebar_buttons[text] = btn
        
        # Highlight the default button if specified
        if default_selected and default_selected in sidebar_buttons:
            self.highlight_sidebar_button(sidebar_buttons, default_selected)
        
        return sidebar, sidebar_buttons
    
    def highlight_sidebar_button(self, buttons, selected):
        """Highlight the selected button in the sidebar"""
        for name, button in buttons.items():
            if name == selected:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                button.configure(fg_color="transparent")
                
    def create_content_area(self):
        """Create a main content area"""
        content = ctk.CTkFrame(self)
        content.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        return content 