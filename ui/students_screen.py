import tkinter as tk
import customtkinter as ctk
from ui.base_screen import BaseScreen
from ui.custom_functions import CustomFunctions
from db.student_repository import StudentRepository

class StudentsScreen(BaseScreen):
    """
    Screen for managing student records
    """
    
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)
        
        # Initialize the student repository
        self.student_repo = StudentRepository()
        
        # Get students from database
        self.students = self.student_repo.get_all()
        
        # If the database is empty, use sample data
        if not self.students:
            self.students = [
                {"id": "001", "name": "John Smith", "class": "10A", "phone": "1234567890", "status": "Active"},
                {"id": "002", "name": "Sarah Johnson", "class": "9B", "phone": "2345678901", "status": "Active"},
                {"id": "003", "name": "Michael Brown", "class": "11A", "phone": "3456789012", "status": "Inactive"},
                {"id": "004", "name": "Emily Davis", "class": "10B", "phone": "4567890123", "status": "Active"},
                {"id": "005", "name": "Daniel Wilson", "class": "12A", "phone": "5678901234", "status": "Active"}
            ]
            
            # Add sample data to database if it's empty
            self.add_sample_data()
        
        # Create header
        self.header = self.create_header("Student Management")
        
        # Create back button at the top
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(side="top", fill="x", padx=20, pady=(0, 10))
        
        self.back_button = ctk.CTkButton(
            self.top_frame,
            text="Back to Dashboard",
            command=self.back_to_dashboard,
            width=150
        )
        self.back_button.pack(side="left", padx=10, pady=10)
        
        # Create main content area
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create action buttons
        self.action_bar = ctk.CTkFrame(self.content)
        self.action_bar.pack(fill="x", padx=10, pady=10)
        
        self.add_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Add Student",
            self.add_student_dialog,
            width=150
        )
        self.add_button.pack(side="left", padx=10)
        
        self.edit_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Edit Selected",
            self.edit_student_dialog,
            width=150,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=10)
        
        self.delete_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Delete Selected",
            self.delete_student,
            width=150,
            fg_color="#E76F51",
            hover_color="#D65F41",
            state="disabled"
        )
        self.delete_button.pack(side="left", padx=10)
        
        # Search bar
        self.search_frame = ctk.CTkFrame(self.action_bar)
        self.search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search students...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = CustomFunctions.create_custom_button(
            self.search_frame,
            "Search",
            self.search_students,
            width=100
        )
        self.search_button.pack(side="left")
        
        # Students table
        self.table_frame = ctk.CTkFrame(self.content)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers
        columns = ["ID", "Name", "Class", "Phone", "Status", "Actions"]
        widths = [100, 200, 100, 150, 100, 150]
        
        self.table_header = CustomFunctions.create_table_header(
            self.table_frame,
            columns,
            widths
        )
        
        # Create scrollable frame for table rows
        self.table_container = ctk.CTkScrollableFrame(self.table_frame)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Status indicator frame at the bottom
        self.status_frame = ctk.CTkFrame(self.content, height=30)
        self.status_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="📡 Real-time updates enabled",
            font=ctk.CTkFont(size=12),
            text_color="#4CC9F0"
        )
        self.status_label.pack(side="right", padx=10, pady=5)
        
        # Total students count
        self.count_label = ctk.CTkLabel(
            self.status_frame,
            text=f"Total students: {len(self.students)}",
            font=ctk.CTkFont(size=12)
        )
        self.count_label.pack(side="left", padx=10, pady=5)
        
        # Populate table with student data
        self.populate_table()
        
        # Subscribe to real-time updates
        self.unsubscribe_function = self.student_repo.subscribe_to_changes(self.handle_data_update)
    
    def handle_data_update(self, updated_students):
        """Handle real-time updates from Firebase"""
        try:
            # Store the updated data
            self.students = updated_students if updated_students else []
            
            # Schedule UI updates on the main thread
            self.after(100, self._update_ui_after_data_change)
        except Exception as e:
            print(f"Error in handle_data_update: {e}")
    
    def _update_ui_after_data_change(self):
        """Update UI elements on the main thread"""
        try:
            # Update the UI with the new data
            self.populate_table()
            self.count_label.configure(text=f"Total students: {len(self.students)}")
            self.show_update_notification()
        except Exception as e:
            print(f"Error updating UI after data change: {e}")
    
    def add_sample_data(self):
        """Add sample data to database if it's empty"""
        for student in self.students:
            # Make a copy of the data without ID since Firestore will generate one
            student_data = student.copy()
            if 'id' in student_data:
                del student_data['id']
            
            # Add to database
            new_id = self.student_repo.add(student_data)
            
            # Update the ID in our local data if successful
            if new_id:
                student['id'] = new_id
    
    def populate_table(self):
        """Populate the table with student data"""
        try:
            # Clear existing data
            for item in self.table_container.winfo_children():
                item.destroy()
            
            # Get students from repository
            students = self.student_repo.get_all()
            
            if not students:
                # Show a message if no students are found
                self.status_label.configure(text="No students found")
                return
            
            # Check what keys are actually in the student data
            if students and len(students) > 0:
                sample_student = students[0]
                print(f"Available student keys: {sample_student.keys()}")
            
            # Add students to table
            for i, student in enumerate(students):
                # Handle the case where 'name' field might not exist
                name = student.get("name", "No Name")
                class_name = student.get("class", "Not Assigned")
                status = student.get("status", "Unknown")
                id_value = student.get("id", "")
                
                # Insert into table with appropriate values
                row_color = "#F8F9FA" if i % 2 == 0 else "#FFFFFF"
                row_frame = ctk.CTkFrame(self.table_container, fg_color=row_color)
                row_frame.pack(fill="x", pady=1)
                
                # Student ID
                id_label = ctk.CTkLabel(
                    row_frame,
                    text=id_value,
                    width=100
                )
                id_label.pack(side="left", padx=5, pady=10)
                
                # Student Name
                name_label = ctk.CTkLabel(
                    row_frame,
                    text=name,
                    width=200,
                    anchor="w"
                )
                name_label.pack(side="left", padx=5, pady=10)
                
                # Class
                class_label = ctk.CTkLabel(
                    row_frame,
                    text=class_name,
                    width=100
                )
                class_label.pack(side="left", padx=5, pady=10)
                
                # Phone
                phone_label = ctk.CTkLabel(
                    row_frame,
                    text=student.get("phone", "N/A"),
                    width=150
                )
                phone_label.pack(side="left", padx=5, pady=10)
                
                # Status
                status_color = "#4CC9F0" if status == "Active" else "#F72585"
                status_label = ctk.CTkLabel(
                    row_frame,
                    text=status,
                    width=100,
                    text_color=status_color,
                    font=ctk.CTkFont(weight="bold")
                )
                status_label.pack(side="left", padx=5, pady=10)
                
                # Action buttons frame
                action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                action_frame.pack(side="left", padx=5, pady=5, fill="x", expand=True)
                
                # View button
                view_btn = ctk.CTkButton(
                    action_frame,
                    text="View",
                    width=70,
                    height=25,
                    font=ctk.CTkFont(size=12),
                    command=lambda s=student: self.view_student(s)
                )
                view_btn.pack(side="left", padx=5)
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    action_frame,
                    text="Edit",
                    width=70,
                    height=25,
                    font=ctk.CTkFont(size=12),
                    command=lambda s=student: self.edit_student_dialog(s)
                )
                edit_btn.pack(side="left", padx=5)
            
            # Update status
            self.status_label.configure(text=f"Showing {len(students)} students")
        except Exception as e:
            # Show error in status label
            self.status_label.configure(text=f"Error loading students: {e}")
            print(f"Error populating table: {e}")
    
    def add_student_dialog(self):
        """Show dialog to add a new student"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Student")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        CustomFunctions.center_window(dialog)
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form title
        title_label = ctk.CTkLabel(
            form_frame,
            text="Add New Student",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=10)
        
        # Configure grid layout for the form
        fields_frame.columnconfigure(0, weight=1)
        fields_frame.columnconfigure(1, weight=3)
        
        # Name field
        name_label = ctk.CTkLabel(fields_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        name_entry = ctk.CTkEntry(fields_frame, width=300)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Class field
        class_label = ctk.CTkLabel(fields_frame, text="Class:")
        class_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        class_entry = ctk.CTkEntry(fields_frame, width=300)
        class_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Phone field
        phone_label = ctk.CTkLabel(fields_frame, text="Phone:")
        phone_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        phone_entry = ctk.CTkEntry(fields_frame, width=300)
        phone_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Status field
        status_label = ctk.CTkLabel(fields_frame, text="Status:")
        status_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        status_var = tk.StringVar(value="Active")
        status_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        status_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        active_radio = ctk.CTkRadioButton(
            status_frame,
            text="Active",
            variable=status_var,
            value="Active"
        )
        active_radio.pack(side="left", padx=(0, 20))
        
        inactive_radio = ctk.CTkRadioButton(
            status_frame,
            text="Inactive",
            variable=status_var,
            value="Inactive"
        )
        inactive_radio.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(30, 20))
        
        # Save button
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save",
            width=100,
            command=lambda: self.save_student(
                dialog,
                {
                    "name": name_entry.get(),
                    "class": class_entry.get(),
                    "phone": phone_entry.get(),
                    "status": status_var.get()
                }
            )
        )
        save_button.pack(side="right", padx=10)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=100,
            fg_color="#E76F51",
            hover_color="#D65F41",
            command=dialog.destroy
        )
        cancel_button.pack(side="right", padx=10)
    
    def edit_student_dialog(self, student):
        """Show dialog to edit a student"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Student")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        CustomFunctions.center_window(dialog)
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form title
        title_label = ctk.CTkLabel(
            form_frame,
            text=f"Edit Student: {student['name']}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=10)
        
        # Configure grid layout for the form
        fields_frame.columnconfigure(0, weight=1)
        fields_frame.columnconfigure(1, weight=3)
        
        # Name field
        name_label = ctk.CTkLabel(fields_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        name_entry = ctk.CTkEntry(fields_frame, width=300)
        name_entry.insert(0, student.get('name', ''))
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Class field
        class_label = ctk.CTkLabel(fields_frame, text="Class:")
        class_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        class_entry = ctk.CTkEntry(fields_frame, width=300)
        class_entry.insert(0, student.get('class', ''))
        class_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Phone field
        phone_label = ctk.CTkLabel(fields_frame, text="Phone:")
        phone_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        phone_entry = ctk.CTkEntry(fields_frame, width=300)
        phone_entry.insert(0, student.get('phone', ''))
        phone_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Status field
        status_label = ctk.CTkLabel(fields_frame, text="Status:")
        status_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        status_var = tk.StringVar(value=student.get('status', 'Active'))
        status_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        status_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        active_radio = ctk.CTkRadioButton(
            status_frame,
            text="Active",
            variable=status_var,
            value="Active"
        )
        active_radio.pack(side="left", padx=(0, 20))
        
        inactive_radio = ctk.CTkRadioButton(
            status_frame,
            text="Inactive",
            variable=status_var,
            value="Inactive"
        )
        inactive_radio.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(30, 20))
        
        # Save button
        save_button = ctk.CTkButton(
            buttons_frame,
            text="Save",
            width=100,
            command=lambda: self.update_student(
                dialog,
                student['id'],
                {
                    "name": name_entry.get(),
                    "class": class_entry.get(),
                    "phone": phone_entry.get(),
                    "status": status_var.get()
                }
            )
        )
        save_button.pack(side="right", padx=10)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=100,
            fg_color="#E76F51",
            hover_color="#D65F41",
            command=dialog.destroy
        )
        cancel_button.pack(side="right", padx=10)
    
    def save_student(self, dialog, student_data):
        """Save a new student to the database"""
        # Validate required fields
        if not student_data['name'] or not student_data['class'] or not student_data['phone']:
            self.show_message("Validation Error", "All fields are required", "error")
            return
        
        # Add student to database
        new_id = self.student_repo.add(student_data)
        
        if new_id:
            # Add ID to the student data
            student_data['id'] = new_id
            
            # Add to our local data
            self.students.append(student_data)
            
            # Refresh the table
            self.populate_table()
            
            # Show success message
            self.show_message("Success", "Student added successfully")
            
            # Close the dialog
            dialog.destroy()
        else:
            self.show_message("Error", "Failed to add student", "error")
    
    def update_student(self, dialog, student_id, student_data):
        """Update a student in the database"""
        # Validate required fields
        if not student_data['name'] or not student_data['class'] or not student_data['phone']:
            self.show_message("Validation Error", "All fields are required", "error")
            return
        
        # Update student in database
        if self.student_repo.update(student_id, student_data):
            # Update in our local data
            for i, student in enumerate(self.students):
                if student['id'] == student_id:
                    # Keep the ID
                    student_data['id'] = student_id
                    self.students[i] = student_data
                    break
            
            # Refresh the table
            self.populate_table()
            
            # Show success message
            self.show_message("Success", "Student updated successfully")
            
            # Close the dialog
            dialog.destroy()
        else:
            self.show_message("Error", "Failed to update student", "error")
    
    def delete_student(self, student=None):
        """Delete a student"""
        if student:
            # Confirm deletion
            if not self.confirm_dialog("Confirm Delete", f"Are you sure you want to delete student {student['name']}?"):
                return
            
            # Delete from database
            if self.student_repo.delete(student['id']):
                # Remove from our local data
                self.students = [s for s in self.students if s['id'] != student['id']]
                
                # Refresh the table
                self.populate_table()
                
                # Show success message
                self.show_message("Success", "Student deleted successfully")
            else:
                self.show_message("Error", "Failed to delete student", "error")
        else:
            self.show_message("Error", "Please select a student to delete", "error")
    
    def view_student(self, student):
        """View a student's details"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Student Details")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        CustomFunctions.center_window(dialog)
        
        # Details frame
        details_frame = ctk.CTkFrame(dialog)
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            details_frame,
            text=f"Student Details: {student['name']}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Details
        info_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # Configure grid layout
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=3)
        
        # ID row
        id_label = ctk.CTkLabel(info_frame, text="ID:", font=ctk.CTkFont(weight="bold"))
        id_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        id_value = ctk.CTkLabel(info_frame, text=student.get('id', 'N/A'))
        id_value.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Name row
        name_label = ctk.CTkLabel(info_frame, text="Name:", font=ctk.CTkFont(weight="bold"))
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        name_value = ctk.CTkLabel(info_frame, text=student.get('name', 'N/A'))
        name_value.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Class row
        class_label = ctk.CTkLabel(info_frame, text="Class:", font=ctk.CTkFont(weight="bold"))
        class_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        class_value = ctk.CTkLabel(info_frame, text=student.get('class', 'N/A'))
        class_value.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Phone row
        phone_label = ctk.CTkLabel(info_frame, text="Phone:", font=ctk.CTkFont(weight="bold"))
        phone_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        phone_value = ctk.CTkLabel(info_frame, text=student.get('phone', 'N/A'))
        phone_value.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Status row
        status_label = ctk.CTkLabel(info_frame, text="Status:", font=ctk.CTkFont(weight="bold"))
        status_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        
        status_color = "#4CC9F0" if student.get('status', '') == "Active" else "#F72585"
        status_value = ctk.CTkLabel(
            info_frame, 
            text=student.get('status', 'N/A'),
            text_color=status_color,
            font=ctk.CTkFont(weight="bold")
        )
        status_value.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Created at row
        if 'created_at' in student:
            created_label = ctk.CTkLabel(info_frame, text="Created:", font=ctk.CTkFont(weight="bold"))
            created_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
            
            created_value = ctk.CTkLabel(info_frame, text=str(student.get('created_at', 'N/A')))
            created_value.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(30, 20))
        
        # Edit button
        edit_button = ctk.CTkButton(
            buttons_frame,
            text="Edit",
            width=100,
            command=lambda: [dialog.destroy(), self.edit_student_dialog(student)]
        )
        edit_button.pack(side="right", padx=10)
        
        # Close button
        close_button = ctk.CTkButton(
            buttons_frame,
            text="Close",
            width=100,
            fg_color="#E76F51",
            hover_color="#D65F41",
            command=dialog.destroy
        )
        close_button.pack(side="right", padx=10)
    
    def search_students(self):
        """Search for students"""
        query = self.search_entry.get()
        
        if not query:
            # If search is empty, refresh with all students
            self.students = self.student_repo.get_all()
        else:
            # Search for students
            self.students = self.student_repo.search(query)
        
        # Refresh the table
        self.populate_table()
        
        # Update count label
        self.count_label.configure(text=f"Total students: {len(self.students)}")
    
    def back_to_dashboard(self):
        """Navigate back to the admin dashboard"""
        self.controller.show_admin()
    
    def destroy(self):
        """Clean up when the screen is destroyed"""
        # Unsubscribe from real-time updates to prevent memory leaks
        if hasattr(self, 'unsubscribe_function') and self.unsubscribe_function:
            try:
                self.unsubscribe_function()
            except Exception as e:
                print(f"Error unsubscribing from real-time updates: {e}")
        
        # Call the parent's destroy method
        super().destroy()

    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Update status first
            self.status_label.configure(text="Loading students data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Get the data
            self.students = self.student_repo.get_all()
            
            # Update UI
            self.populate_table()
            self.count_label.configure(text=f"Total students: {len(self.students)}")
            
            # Update status
            self.status_label.configure(text="Students data loaded", text_color="#4CC9F0")
            self.after(3000, lambda: self.status_label.configure(
                text="📡 Real-time updates enabled",
                text_color="#4CC9F0"
            ))
        except Exception as e:
            print(f"Error loading tab data: {e}")
            self.status_label.configure(text="Error loading data", text_color="#E76F51")

class StudentsComponent(ctk.CTkFrame):
    """
    Component for managing student records - designed to be embedded in a tabbed interface
    """
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # Initialize the student repository
        self.student_repo = StudentRepository()
        
        # Get students from database
        self.students = self.student_repo.get_all()
        # print(f"Students from database: {self.students}")
        
        # If the database is empty, use sample data
        if not self.students:
            print("No students found, using sample data")
            self.students = [
                {"id": "001", "name": "John Smith", "class": "10A", "phone": "1234567890", "status": "Active"},
                {"id": "002", "name": "Sarah Johnson", "class": "9B", "phone": "2345678901", "status": "Active"},
                {"id": "003", "name": "Michael Brown", "class": "11A", "phone": "3456789012", "status": "Inactive"},
                {"id": "004", "name": "Emily Davis", "class": "10B", "phone": "4567890123", "status": "Active"},
                {"id": "005", "name": "Daniel Wilson", "class": "12A", "phone": "5678901234", "status": "Active"}
            ]
            
            # Add sample data to database if it's empty
            self.add_sample_data()
        
        # Create main content area
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Create action buttons
        self.action_bar = ctk.CTkFrame(self.content)
        self.action_bar.pack(fill="x", padx=10, pady=10)
        
        self.add_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Add Student",
            self.add_student_dialog,
            width=150
        )
        self.add_button.pack(side="left", padx=10)
        
        # Search bar
        self.search_frame = ctk.CTkFrame(self.action_bar)
        self.search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search students...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = CustomFunctions.create_custom_button(
            self.search_frame,
            "Search",
            self.search_students,
            width=100
        )
        self.search_button.pack(side="left")
        
        # Students table
        self.table_frame = ctk.CTkFrame(self.content)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers
        columns = ["ID", "Name", "Class", "Phone", "Status", "Actions"]
        widths = [80, 150, 80, 120, 100, 150]
        
        self.table_header = CustomFunctions.create_table_header(
            self.table_frame,
            columns,
            widths
        )
        
        # Create scrollable frame for table rows
        self.table_container = ctk.CTkScrollableFrame(self.table_frame)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Status indicator frame at the bottom
        self.status_frame = ctk.CTkFrame(self.content, height=30)
        self.status_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="📡 Real-time updates enabled",
            font=ctk.CTkFont(size=12),
            text_color="#4CC9F0"
        )
        self.status_label.pack(side="right", padx=10, pady=5)
        
        # Total students count
        self.count_label = ctk.CTkLabel(
            self.status_frame,
            text=f"Total students: {len(self.students)}",
            font=ctk.CTkFont(size=12)
        )
        self.count_label.pack(side="left", padx=10, pady=5)
        
        # Populate table with student data
        self.populate_table()
        
        # Setup real-time updates
        self.setup_data_listener()
    
    def add_sample_data(self):
        """Add sample data to database if it's empty"""
        for student in self.students:
            self.student_repo.add(student)
    
    def setup_data_listener(self):
        """Setup real-time data listener for students"""
        try:
            self.unsubscribe_function = self.student_repo.subscribe_to_changes(self.handle_data_update)
        except Exception as e:
            print(f"Error setting up data listener: {e}")
    
    def handle_data_update(self, updated_students):
        """Handle real-time updates from Firebase"""
        try:
            # Store the updated data
            self.students = updated_students if updated_students else []
            
            # Schedule UI updates on the main thread
            self.after(100, self._update_ui_after_data_change)
        except Exception as e:
            print(f"Error in handle_data_update: {e}")
    
    def _update_ui_after_data_change(self):
        """Update UI elements on the main thread"""
        try:
            # Update the UI with the new data
            self.populate_table()
            self.count_label.configure(text=f"Total students: {len(self.students)}")
            self.show_update_notification()
        except Exception as e:
            print(f"Error updating UI after data change: {e}")
    
    def show_update_notification(self):
        """Show a temporary update notification"""
        self.status_label.configure(text="📡 Data updated in real-time", text_color="#4CC9F0")
        self.after(3000, lambda: self.status_label.configure(
            text="📡 Real-time updates enabled",
            text_color="#4CC9F0"
        ))
    
    def populate_table(self):
        """Populate the table with student data"""
        # Clear existing data
        for item in self.table_container.winfo_children():
            item.destroy()
        
        # Add students to table
        for i, student in enumerate(self.students):
            row = ctk.CTkFrame(self.table_container, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # Add student data
            ctk.CTkLabel(row, text=student.get('id', ''), width=80).pack(side="left")
            ctk.CTkLabel(row, text=student.get('name', ''), width=150).pack(side="left")
            ctk.CTkLabel(row, text=student.get('class', ''), width=80).pack(side="left")
            ctk.CTkLabel(row, text=student.get('phone', ''), width=120).pack(side="left")
            
            # Status with color coding
            status = student.get('status', 'Inactive')
            status_color = "#4CC9F0" if status == "Active" else "#E76F51"
            status_label = ctk.CTkLabel(
                row,
                text=status,
                width=100,
                text_color=status_color
            )
            status_label.pack(side="left")
            
            # Actions frame
            actions_frame = ctk.CTkFrame(row, fg_color="transparent", width=150)
            actions_frame.pack(side="left", fill="x")
            
            # View button
            view_btn = ctk.CTkButton(
                actions_frame,
                text="View",
                width=60,
                height=24,
                command=lambda s=student: self.view_student(s)
            )
            view_btn.pack(side="left", padx=2)
            
            # Edit button
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Edit",
                width=60,
                height=24,
                command=lambda s=student: self.edit_student_dialog(s)
            )
            edit_btn.pack(side="left", padx=2)
    
    def add_student_dialog(self):
        """Show dialog to add a new student"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Student")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ctk.CTkFrame(dialog)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        # Student ID
        id_label = ctk.CTkLabel(content_frame, text="Student ID:")
        id_label.pack(anchor="w", padx=10, pady=(20, 5))
        
        id_entry = ctk.CTkEntry(content_frame, width=350)
        id_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Name
        name_label = ctk.CTkLabel(content_frame, text="Name:")
        name_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        name_entry = ctk.CTkEntry(content_frame, width=350)
        name_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Class
        class_label = ctk.CTkLabel(content_frame, text="Class:")
        class_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        class_var = tk.StringVar(value="10A")
        class_menu = ctk.CTkOptionMenu(
            content_frame,
            variable=class_var,
            values=["9A", "9B", "10A", "10B", "11A", "11B", "12A", "12B"],
            width=350
        )
        class_menu.pack(fill="x", padx=10, pady=(0, 15))
        
        # Phone
        phone_label = ctk.CTkLabel(content_frame, text="Phone:")
        phone_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        phone_entry = ctk.CTkEntry(content_frame, width=350)
        phone_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Status
        status_label = ctk.CTkLabel(content_frame, text="Status:")
        status_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        status_var = tk.StringVar(value="Active")
        
        status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        active_radio = ctk.CTkRadioButton(
            status_frame,
            text="Active",
            variable=status_var,
            value="Active"
        )
        active_radio.pack(side="left", padx=(0, 20))
        
        inactive_radio = ctk.CTkRadioButton(
            status_frame,
            text="Inactive",
            variable=status_var,
            value="Inactive"
        )
        inactive_radio.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(20, 0))
        
        # Add button
        add_button = ctk.CTkButton(
            buttons_frame,
            text="Add Student",
            command=lambda: self.save_student(
                dialog,
                {
                    'id': id_entry.get(),
                    'name': name_entry.get(),
                    'class': class_var.get(),
                    'phone': phone_entry.get(),
                    'status': status_var.get()
                }
            ),
            height=35,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        add_button.pack(side="right", padx=5)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#E76F51",
            hover_color="#D65F41",
            command=dialog.destroy,
            height=35,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        cancel_button.pack(side="right", padx=5)
    
    def save_student(self, dialog, student_data):
        """Save a new student"""
        try:
            # Validate data
            if not student_data['id'] or not student_data['name']:
                messagebox.showerror("Error", "Student ID and Name are required fields")
                return
            
            # Add to database
            result = self.student_repo.add(student_data)
            
            if result:
                # Close dialog
                dialog.destroy()
                messagebox.showinfo("Success", "Student added successfully")
            else:
                messagebox.showerror("Error", "Failed to add student")
        
        except Exception as e:
            print(f"Error saving student: {e}")
            messagebox.showerror("Error", "Failed to save student")
    
    def edit_student_dialog(self, student):
        """Show dialog to edit a student"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Student")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ctk.CTkFrame(dialog)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        # Student ID (read-only)
        id_label = ctk.CTkLabel(content_frame, text="Student ID:")
        id_label.pack(anchor="w", padx=10, pady=(20, 5))
        
        id_entry = ctk.CTkEntry(content_frame, width=350)
        id_entry.insert(0, student['id'])
        id_entry.configure(state="disabled")
        id_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Name
        name_label = ctk.CTkLabel(content_frame, text="Name:")
        name_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        name_entry = ctk.CTkEntry(content_frame, width=350)
        name_entry.insert(0, student['name'])
        name_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Class
        class_label = ctk.CTkLabel(content_frame, text="Class:")
        class_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        class_var = tk.StringVar(value=student['class'])
        class_menu = ctk.CTkOptionMenu(
            content_frame,
            variable=class_var,
            values=["9A", "9B", "10A", "10B", "11A", "11B", "12A", "12B"],
            width=350
        )
        class_menu.pack(fill="x", padx=10, pady=(0, 15))
        
        # Phone
        phone_label = ctk.CTkLabel(content_frame, text="Phone:")
        phone_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        phone_entry = ctk.CTkEntry(content_frame, width=350)
        phone_entry.insert(0, student['phone'])
        phone_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Status
        status_label = ctk.CTkLabel(content_frame, text="Status:")
        status_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        status_var = tk.StringVar(value=student['status'])
        
        status_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        active_radio = ctk.CTkRadioButton(
            status_frame,
            text="Active",
            variable=status_var,
            value="Active"
        )
        active_radio.pack(side="left", padx=(0, 20))
        
        inactive_radio = ctk.CTkRadioButton(
            status_frame,
            text="Inactive",
            variable=status_var,
            value="Inactive"
        )
        inactive_radio.pack(side="left")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(20, 0))
        
        # Update button
        update_button = ctk.CTkButton(
            buttons_frame,
            text="Update Student",
            command=lambda: self.update_student(
                dialog,
                student['id'],
                {
                    'name': name_entry.get(),
                    'class': class_var.get(),
                    'phone': phone_entry.get(),
                    'status': status_var.get()
                }
            ),
            height=35,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        update_button.pack(side="right", padx=5)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#E76F51",
            hover_color="#D65F41",
            command=dialog.destroy,
            height=35,
            font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        cancel_button.pack(side="right", padx=5)
    
    def update_student(self, dialog, student_id, student_data):
        """Update an existing student"""
        try:
            # Validate data
            if not student_data['name']:
                messagebox.showerror("Error", "Name is a required field")
                return
            
            # Update in database
            if self.student_repo.update(student_id, student_data):
                # Close dialog
                dialog.destroy()
                messagebox.showinfo("Success", "Student updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update student")
        
        except Exception as e:
            print(f"Error updating student: {e}")
            messagebox.showerror("Error", "Failed to update student")
    
    def view_student(self, student):
        """View a student's details"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Student Details")
        dialog.geometry("400x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ctk.CTkFrame(dialog)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Student details
        details = [
            ("Student ID", student['id']),
            ("Name", student['name']),
            ("Class", student['class']),
            ("Phone", student['phone']),
            ("Status", student['status'])
        ]
        
        for label, value in details:
            # Label
            ctk.CTkLabel(
                content_frame,
                text=label + ":",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w", padx=10, pady=(15, 0))
            
            # Value
            value_color = "#4CC9F0" if label == "Status" and value == "Active" else "white"
            if label == "Status" and value == "Inactive":
                value_color = "#E76F51"
                
            ctk.CTkLabel(
                content_frame,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color=value_color
            ).pack(anchor="w", padx=20, pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(30, 0))
        
        # Edit button
        edit_button = ctk.CTkButton(
            buttons_frame,
            text="Edit",
            command=lambda: [dialog.destroy(), self.edit_student_dialog(student)],
            width=100
        )
        edit_button.pack(side="right", padx=10)
        
        # Close button
        close_button = ctk.CTkButton(
            buttons_frame,
            text="Close",
            width=100,
            fg_color="#E76F51",
            hover_color="#D65F41",
            command=dialog.destroy
        )
        close_button.pack(side="right", padx=10)
    
    def search_students(self):
        """Search for students"""
        query = self.search_entry.get()
        
        if not query:
            # If search is empty, refresh with all students
            self.students = self.student_repo.get_all()
        else:
            # Search for students
            self.students = self.student_repo.search(query)
        
        # Refresh the table
        self.populate_table()
        
        # Update count label
        self.count_label.configure(text=f"Total students: {len(self.students)}")
    
    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Update status first
            self.status_label.configure(text="Loading students data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Get the data
            self.students = self.student_repo.get_all()
            
            # Update UI
            self.populate_table()
            self.count_label.configure(text=f"Total students: {len(self.students)}")
            
            # Update status
            self.status_label.configure(text="Students data loaded", text_color="#4CC9F0")
            self.after(3000, lambda: self.status_label.configure(
                text="📡 Real-time updates enabled",
                text_color="#4CC9F0"
            ))
        except Exception as e:
            print(f"Error loading tab data: {e}")
            self.status_label.configure(text="Error loading data", text_color="#E76F51")
    
    def cleanup(self):
        """Clean up resources when component is no longer needed"""
        if hasattr(self, 'unsubscribe_function') and self.unsubscribe_function:
            try:
                self.unsubscribe_function()
                print("Unsubscribed from students updates")
            except Exception as e:
                print(f"Error unsubscribing from updates: {e}") 