import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # Remove previous packing as it's causing issues
        # Instead, configure this frame for grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create main frame for login with fixed width and height
        self.login_frame = ctk.CTkFrame(self, corner_radius=15, width=600, height=500)
        
        # Center the login frame in the parent window
        self.login_frame.grid(row=0, column=0, sticky="")
        
        # Prevent the frame from shrinking to fit its children
        self.login_frame.grid_propagate(False)
        
        # Configure grid for login frame
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.login_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Title label (spans both columns)
        self.title_label = ctk.CTkLabel(
            self.login_frame, 
            text="Smart Result System",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(40, 20), padx=10)
        
        # Subtitle (spans both columns)
        self.subtitle = ctk.CTkLabel(
            self.login_frame, 
            text="Login",
            font=ctk.CTkFont(size=16)
        )
        self.subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 30), padx=10)
        
        # Email label and entry
        self.email_label = ctk.CTkLabel(
            self.login_frame, 
            text="Email:",
            font=ctk.CTkFont(size=14)
        )
        self.email_label.grid(row=2, column=0, pady=10, padx=10, sticky="e")
        
        self.email_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter your email",
            width=300,
            height=40,
            border_width=1
        )
        self.email_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        
        # Password label and entry
        self.password_label = ctk.CTkLabel(
            self.login_frame, 
            text="Password:",
            font=ctk.CTkFont(size=14)
        )
        self.password_label.grid(row=3, column=0, pady=10, padx=10, sticky="e")
        
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter your password",
            width=300,
            height=40,
            border_width=1,
            show="•"
        )
        self.password_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        
        # Remember me checkbox
        self.remember_var = tk.IntVar()
        self.remember_checkbox = ctk.CTkCheckBox(
            self.login_frame,
            text="Remember me",
            variable=self.remember_var
        )
        self.remember_checkbox.grid(row=4, column=0, columnspan=2, pady=(10, 20), padx=100, sticky="w")
        
        # Login button (spans both columns)
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            height=40,
            command=self.login
        )
        self.login_button.grid(row=5, column=0, columnspan=2, pady=(20, 10), padx=10)
        
        # Status message label
        self.status_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#E76F51"
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=(0, 10), padx=10)
        
        # Info label for demo credentials
        self.demo_label = ctk.CTkLabel(
            self.login_frame,
            text="Demo credentials: admin / admin",
            font=ctk.CTkFont(size=10),
            text_color="#6c757d"
        )
        self.demo_label.grid(row=7, column=0, columnspan=2, pady=(0, 5), padx=10)
    
    def login(self):
        """Handle login functionality with hardcoded credentials"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            self.show_status("Please enter both email and password", "error")
            return
        
        # Simple hardcoded authentication
        if email == "admin" and password == "admin":
            user = {
                'uid': 'admin-uid',
                'email': 'admin@smr.com',
                'name': 'Administrator',
                'role': 'admin'
            }
            self.login_success(user)
        elif email == "teacher@smr.com" and password == "teacher123":
            user = {
                'uid': 'teacher-uid',
                'email': 'teacher@smr.com',
                'name': 'Demo Teacher',
                'role': 'teacher'
            }
            self.login_success(user)
        else:
            self.show_status("Invalid credentials. Please try again.", "error")
    
    def login_success(self, user):
        """Handle successful login"""
        # Set user in the controller
        self.controller.current_user = user
        
        # Get user role
        role = user.get('role', 'unknown')
        
        # Show success message
        self.show_status(f"Login successful! Redirecting to {role} dashboard...", "success")
        
        # Redirect to appropriate dashboard after a brief delay
        self.after(1000, lambda: self.redirect_to_dashboard(role))
    
    def redirect_to_dashboard(self, role):
        """Redirect to the appropriate dashboard based on role"""
        if role == "admin":
            self.controller.show_frame("admin")
        elif role == "teacher":
            self.controller.show_frame("teacher")
        else:
            # Default to admin if unknown role
            self.controller.show_frame("admin")
    
    def show_status(self, message, message_type="info"):
        """Show status message with appropriate styling"""
        self.status_label.configure(text=message)
        
        if message_type == "error":
            self.status_label.configure(text_color="#E76F51")  # Red for errors
        elif message_type == "success":
            self.status_label.configure(text_color="#2A9D8F")  # Green for success
        else:
            self.status_label.configure(text_color="#3A86FF")  # Blue for info 