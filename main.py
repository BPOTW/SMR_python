import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from ui.admin_dashboard import AdminDashboard
from db.firebase_config import FirebaseConfig
import os
import sys
import json

class SmartResultSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Result System")
        
        # Initialize Firebase database
        self.initialize_firebase()
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to screen size but keep the window decorations
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Maximize the window
        # self.root.state('zoomed')  # This works on Windows
        
        # Set the theme mode
        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Create and initialize the admin dashboard directly
        self.admin_dashboard = AdminDashboard(self.root, self)
        self.admin_dashboard.pack(fill="both", expand=True)
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def initialize_firebase(self):
        """Initialize Firebase database configuration"""
        try:
            # Check if service account file exists
            service_account_path = 'firebase-credentials.json'
            
            if os.path.exists(service_account_path):
                # Initialize Firebase with credentials file
                FirebaseConfig.initialize(credentials_path=service_account_path)
                print("Firebase initialized with credentials file.")
            else:
                # Create a sample service account file for demonstration
                self.create_sample_firebase_credentials()
                
                if os.path.exists(service_account_path):
                    FirebaseConfig.initialize(credentials_path=service_account_path)
                    print("Firebase initialized with sample credentials file.")
                else:
                    # Initialize Firebase with default configuration (for testing/development)
                    FirebaseConfig.initialize()
                    print("Firebase initialized with default configuration.")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            print("Using mock implementation instead.")
            FirebaseConfig.initialize()
    
    def create_sample_firebase_credentials(self):
        """
        Create a sample Firebase credentials file for demonstration purposes.
        In a real application, these credentials should be obtained from Firebase console.
        """
        try:
            # Sample credentials for demonstration (these are fake)
            sample_creds = {
                "type": "service_account",
                "project_id": "smart-result-system-demo",
                "private_key_id": "sample-key-id-for-demonstration",
                "private_key": "-----BEGIN PRIVATE KEY-----\nSAMPLE_KEY_FOR_DEMO_ONLY\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-sample@smart-result-system-demo.iam.gserviceaccount.com",
                "client_id": "123456789012345678901",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-sample%40smart-result-system-demo.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
            
            # Write to a file
            with open('firebase-credentials.json', 'w') as f:
                json.dump(sample_creds, f, indent=2)
            
            print("Sample Firebase credentials file created for demonstration.")
        except Exception as e:
            print(f"Error creating sample Firebase credentials: {e}")
    
    def on_closing(self):
        """Handle window close event"""
        try:
            # Clean up resources
            if hasattr(self, 'admin_dashboard'):
                self.admin_dashboard.cleanup()
            
            # Close the application
            self.root.destroy()
        except Exception as e:
            print(f"Error during application shutdown: {e}")
            self.root.destroy()

if __name__ == "__main__":
    # Create the root window
    root = ctk.CTk()
    app = SmartResultSystem(root)
    root.mainloop() 