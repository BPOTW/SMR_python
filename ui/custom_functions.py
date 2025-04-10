import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import datetime
from db.teacher_repository import TeacherRepository

class CustomFunctions:
    """
    A utility class containing custom functions that can be used across
    different screens in the Smart Result System
    """
    
    @staticmethod
    def format_date(date=None):
        """Format date to a readable string"""
        if date is None:
            date = datetime.datetime.now()
        return date.strftime("%d %B, %Y")
    
    @staticmethod
    def create_custom_button(parent, text, command, **kwargs):
        """Create a custom styled button"""
        default_kwargs = {
            "fg_color": "#3B8ED0",
            "hover_color": "#1F6AA5",
            "height": 40,
            "corner_radius": 8
        }
        # Update with any additional kwargs
        default_kwargs.update(kwargs)
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            **default_kwargs
        )
        return button
    
    @staticmethod
    def create_card(parent, title, value, color="#4361EE", **kwargs):
        """Create a statistic card with title and value"""
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=10, **kwargs)
        
        # Card title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16),
            text_color="#FFFFFF"
        )
        title_label.pack(pady=(15, 5), padx=20)
        
        # Card value
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        )
        value_label.pack(pady=(0, 15), padx=20)
        
        return card
    
    @staticmethod
    def create_table_header(parent, columns, widths):
        """Create a table header with given columns and widths"""
        header_frame = ctk.CTkFrame(parent, fg_color="#E0E0E0")
        header_frame.pack(fill="x", padx=20, pady=(0, 2))
        
        for i, (column, width) in enumerate(zip(columns, widths)):
            header_label = ctk.CTkLabel(
                header_frame,
                text=column,
                width=width,
                font=ctk.CTkFont(weight="bold")
            )
            header_label.pack(side="left", padx=5, pady=10)
        
        return header_frame
    
    @staticmethod
    def create_table_row(parent, data, widths, row_color="#FFFFFF"):
        """Create a table row with given data and widths"""
        row_frame = ctk.CTkFrame(parent, fg_color=row_color)
        row_frame.pack(fill="x", padx=20, pady=1)
        
        for i, (cell, width) in enumerate(zip(data, widths)):
            cell_label = ctk.CTkLabel(
                row_frame,
                text=str(cell),
                width=width,
                anchor="w"
            )
            cell_label.pack(side="left", padx=5, pady=10)
        
        return row_frame
    
    @staticmethod
    def show_message(title, message, message_type="info"):
        """Show a message dialog"""
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        elif message_type == "error":
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)
    
    @staticmethod
    def confirm_dialog(title, message):
        """Show a confirmation dialog"""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def input_dialog(title, message):
        """Show an input dialog"""
        return simpledialog.askstring(title, message)
    
    @staticmethod
    def validate_input(input_type, value):
        """Validate input based on input type"""
        if input_type == "phone":
            # Simple phone validation (digits only)
            return value.isdigit()
        elif input_type == "email":
            # Simple email validation
            return "@" in value and "." in value
        elif input_type == "name":
            # Name validation (not empty)
            return len(value.strip()) > 0
        else:
            return True
    
    @staticmethod
    def center_window(window):
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


    #custom functions
    #get list of teacher names from database
    @staticmethod
    def get_teacher_names():
        """
        Retrieves a list of all teacher names from the database.

        Requires 'from db.teacher_repository import TeacherRepository' to be imported
        at the top level of this file.

        Returns:
            list: A list of teacher names, or an empty list if an error occurs
                  or no teachers are found.
        """
        # Note: Assumes TeacherRepository is imported at the top of the file
        # from db.teacher_repository import TeacherRepository
        try:
            teacher_repo = TeacherRepository()
            all_teachers = teacher_repo.get_all() # Gets list of teacher dicts
            
            if not all_teachers:
                print("No teachers found in the database.")
                return []
                
            # Extract the 'name' field from each teacher dictionary
            teacher_names = [teacher.get('name', 'Unknown Name') for teacher in all_teachers if isinstance(teacher, dict)]
            # print(teacher_names)
            return teacher_names
        except NameError:
             print("Error: TeacherRepository class not found. Ensure it's imported.")
             # In a real scenario, might want to raise the error or log it more formally
             return []
        except Exception as e:
            print(f"An error occurred while fetching teacher names: {e}")
            # Depending on requirements, might show an error message to the user
            # CustomFunctions.show_message("Error", f"Failed to load teacher names: {e}", "error")
            return []
        
        
    
    
    
