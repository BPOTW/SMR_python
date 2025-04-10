import tkinter as tk
import customtkinter as ctk
from ui.base_screen import BaseScreen
from ui.custom_functions import CustomFunctions
import tkinter.messagebox as messagebox
from db.teacher_repository import TeacherRepository

class TeachersScreen(BaseScreen):
    """
    Screen for managing teacher records
    """
    
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)
        
        # Sample teacher data
        self.teachers = [
            {"id": "T001", "name": "Dr. Robert Miller", "subject": "Mathematics", "phone": "1234567890", "status": "Active"},
            {"id": "T002", "name": "Dr. Jennifer Lee", "subject": "Science", "phone": "2345678901", "status": "Active"},
            {"id": "T003", "name": "Prof. David Clark", "subject": "History", "phone": "3456789012", "status": "Inactive"},
            {"id": "T004", "name": "Ms. Amanda White", "subject": "English", "phone": "4567890123", "status": "Active"},
            {"id": "T005", "name": "Mr. James Thompson", "subject": "Physics", "phone": "5678901234", "status": "Active"}
        ]
        
        # Create header
        self.header = self.create_header("Teacher Management")
        
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
            "Add Teacher",
            self.add_teacher,
            width=150
        )
        self.add_button.pack(side="left", padx=10)
        
        self.edit_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Edit Selected",
            self.edit_teacher,
            width=150,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=10)
        
        self.delete_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Delete Selected",
            self.delete_teacher,
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
            placeholder_text="Search teachers...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = CustomFunctions.create_custom_button(
            self.search_frame,
            "Search",
            self.search_teachers,
            width=100
        )
        self.search_button.pack(side="left")
        
        # Teachers table
        self.table_frame = ctk.CTkFrame(self.content)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers
        columns = ["ID", "Name", "Subject", "Phone", "Status", "Actions"]
        widths = [100, 200, 150, 150, 100, 150]
        
        self.table_header = CustomFunctions.create_table_header(
            self.table_frame,
            columns,
            widths
        )
        
        # Create scrollable frame for table rows
        self.table_container = ctk.CTkScrollableFrame(self.table_frame)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Populate table with teacher data
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with teacher data"""
        try:
            # Clear existing rows
            for widget in self.table_container.winfo_children():
                widget.destroy()
            
            # Add rows for each teacher
            for i, teacher in enumerate(self.teachers):
                print(f"Processing teacher: {teacher}")
                row_color = "#F8F9FA" if i % 2 == 0 else "#FFFFFF"
                row_frame = ctk.CTkFrame(self.table_container, fg_color=row_color)
                row_frame.pack(fill="x", pady=1)
                
                # Teacher ID
                id_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("id", "N/A"),
                    width=100
                )
                id_label.pack(side="left", padx=5, pady=10)
                
                # Teacher Name
                name_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("name", "Unknown"),
                    width=200,
                    anchor="w"
                )
                name_label.pack(side="left", padx=5, pady=10)
                
                # Subject
                subject_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("subject", "N/A"),
                    width=150
                )
                subject_label.pack(side="left", padx=5, pady=10)
                
                # Phone
                phone_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("phone", "N/A"),
                    width=150
                )
                phone_label.pack(side="left", padx=5, pady=10)
                
                # Status
                status = teacher.get("status", "Inactive")
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
                    command=lambda t=teacher: self.view_teacher(t)
                )
                view_btn.pack(side="left", padx=5)
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    action_frame,
                    text="Edit",
                    width=70,
                    height=25,
                    font=ctk.CTkFont(size=12),
                    command=lambda t=teacher: self.edit_teacher(t)
                )
                edit_btn.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error in populate_table: {e}")
            messagebox.showerror("Error", f"Failed to populate teachers table: {e}")
    
    def add_teacher(self):
        """Add a new teacher"""
        self.show_message("Add Teacher", "This feature will be implemented in a future update.")
    
    def edit_teacher(self, teacher=None):
        """Edit a teacher record"""
        if teacher:
            self.show_message("Edit Teacher", f"Editing {teacher['name']}")
        else:
            self.show_message("Edit Teacher", "Please select a teacher to edit.")
    
    def delete_teacher(self):
        """Delete a teacher record"""
        self.show_message("Delete Teacher", "This feature will be implemented in a future update.")
    
    def view_teacher(self, teacher):
        """View a teacher's details"""
        self.show_message("Teacher Details", f"Viewing details for {teacher['name']}")
    
    def search_teachers(self):
        """Search for teachers"""
        try:
            search_term = self.search_entry.get().lower()
            if not search_term:
                # If search is empty, show all teachers
                self.populate_table()
                return
            
            # Filter teachers based on search term
            filtered_teachers = []
            
            for teacher in self.teachers:
                if isinstance(teacher, dict):
                    if (search_term in teacher.get("name", "").lower() or
                        search_term in teacher.get("id", "").lower() or
                        search_term in teacher.get("subject", "").lower() or
                        search_term in teacher.get("phone", "").lower() or
                        search_term in teacher.get("status", "").lower()):
                        filtered_teachers.append(teacher)
            
            # Update teachers list temporarily for display
            original_teachers = self.teachers
            self.teachers = filtered_teachers
            
            # Repopulate the table with filtered results
            self.populate_table()
            
            # Restore original list
            self.teachers = original_teachers
        except Exception as e:
            print(f"Error in search_teachers: {e}")
            # Reset to original data
            self.populate_table()
    
    def back_to_dashboard(self):
        """Navigate back to the admin dashboard"""
        self.controller.show_admin() 

    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Update status first
            self.status_label.configure(text="Loading teachers data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Get the data
            self.teachers = self.teacher_repo.get_all()
            
            # Update UI
            self.populate_table()
            self.count_label.configure(text=f"Total teachers: {len(self.teachers)}")
            
            # Update status
            self.status_label.configure(text="Teachers tab activated", text_color="#4CC9F0")
            self.after(3000, lambda: self.status_label.configure(
                text="Teachers Component Ready",
                text_color="#4CC9F0"
            ))
        except Exception as e:
            print(f"Error loading tab data: {e}")
            self.status_label.configure(text="Error loading data", text_color="#E76F51")

class TeachersComponent(ctk.CTkFrame):
    """
    Component for managing teacher records
    """
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # Initialize the teacher repository
        self.teacher_repo = TeacherRepository()
        
        # Get teachers from database
        self.teachers = self.teacher_repo.get_all()
        # print(f"Teachers from database: {self.teachers}")
        
        # If the database is empty, use sample data
        if not self.teachers:
            print("No teachers found, using sample data")
            self.teachers = [
                {"id": "T001", "name": "Dr. Robert Miller", "subject": "Mathematics", "phone": "1234567890", "status": "Active"},
                {"id": "T002", "name": "Dr. Jennifer Lee", "subject": "Science", "phone": "2345678901", "status": "Active"},
                {"id": "T003", "name": "Prof. David Clark", "subject": "History", "phone": "3456789012", "status": "Inactive"},
                {"id": "T004", "name": "Ms. Amanda White", "subject": "English", "phone": "4567890123", "status": "Active"},
                {"id": "T005", "name": "Mr. James Thompson", "subject": "Physics", "phone": "5678901234", "status": "Active"}
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
            "Add Teacher",
            self.add_teacher,
            width=150
        )
        self.add_button.pack(side="left", padx=10)
        
        self.edit_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Edit Selected",
            self.edit_teacher,
            width=150,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=10)
        
        self.delete_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Delete Selected",
            self.delete_teacher,
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
            placeholder_text="Search teachers...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = CustomFunctions.create_custom_button(
            self.search_frame,
            "Search",
            self.search_teachers,
            width=100
        )
        self.search_button.pack(side="left")
        
        # Teachers table
        self.table_frame = ctk.CTkFrame(self.content)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers
        columns = ["ID", "Name", "Subject", "Phone", "Status", "Actions"]
        widths = [100, 200, 150, 150, 100, 150]
        
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
            text="Teachers Component Ready",
            font=ctk.CTkFont(size=12),
            text_color="#4CC9F0"
        )
        self.status_label.pack(side="right", padx=10, pady=5)
        
        # Total teachers count
        self.count_label = ctk.CTkLabel(
            self.status_frame,
            text=f"Total teachers: {len(self.teachers)}",
            font=ctk.CTkFont(size=12)
        )
        self.count_label.pack(side="left", padx=10, pady=5)
        
        # Populate table with teacher data
        self.populate_table()
        
        # Setup real-time updates
        self.setup_data_listener()
    
    def populate_table(self):
        """Populate the table with teacher data"""
        try:
            # Clear existing rows
            for widget in self.table_container.winfo_children():
                widget.destroy()
            
            # Add rows for each teacher
            for i, teacher in enumerate(self.teachers):
                # print(f"Processing teacher: {teacher}")
                row_color = "#F8F9FA" if i % 2 == 0 else "#FFFFFF"
                row_frame = ctk.CTkFrame(self.table_container, fg_color=row_color)
                row_frame.pack(fill="x", pady=1)
                
                # Teacher ID
                id_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("id", "N/A"),
                    width=100
                )
                id_label.pack(side="left", padx=5, pady=10)
                
                # Teacher Name
                name_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("name", "Unknown"),
                    width=200,
                    anchor="w"
                )
                name_label.pack(side="left", padx=5, pady=10)
                
                # Subject
                subject_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("subject", "N/A"),
                    width=150
                )
                subject_label.pack(side="left", padx=5, pady=10)
                
                # Phone
                phone_label = ctk.CTkLabel(
                    row_frame,
                    text=teacher.get("phone", "N/A"),
                    width=150
                )
                phone_label.pack(side="left", padx=5, pady=10)
                
                # Status
                status = teacher.get("status", "Inactive")
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
                    command=lambda t=teacher: self.view_teacher(t)
                )
                view_btn.pack(side="left", padx=5)
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    action_frame,
                    text="Edit",
                    width=70,
                    height=25,
                    font=ctk.CTkFont(size=12),
                    command=lambda t=teacher: self.edit_teacher(t)
                )
                edit_btn.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error in populate_table: {e}")
            messagebox.showerror("Error", f"Failed to populate teachers table: {e}")
    
    def add_teacher(self):
        """Add a new teacher"""
        self.show_message("Add Teacher", "This feature will be implemented in a future update.")
    
    def edit_teacher(self, teacher=None):
        """Edit a teacher record"""
        if teacher:
            self.show_message("Edit Teacher", f"Editing {teacher['name']}")
        else:
            self.show_message("Edit Teacher", "Please select a teacher to edit.")
    
    def delete_teacher(self):
        """Delete a teacher record"""
        self.show_message("Delete Teacher", "This feature will be implemented in a future update.")
    
    def view_teacher(self, teacher):
        """View a teacher's details"""
        self.show_message("Teacher Details", f"Viewing details for {teacher['name']}")
    
    def search_teachers(self):
        """Search for teachers"""
        try:
            search_term = self.search_entry.get().lower()
            if not search_term:
                # If search is empty, show all teachers
                self.populate_table()
                return
            
            # Filter teachers based on search term
            filtered_teachers = []
            
            for teacher in self.teachers:
                if isinstance(teacher, dict):
                    if (search_term in teacher.get("name", "").lower() or
                        search_term in teacher.get("id", "").lower() or
                        search_term in teacher.get("subject", "").lower() or
                        search_term in teacher.get("phone", "").lower() or
                        search_term in teacher.get("status", "").lower()):
                        filtered_teachers.append(teacher)
            
            # Update teachers list temporarily for display
            original_teachers = self.teachers
            self.teachers = filtered_teachers
            
            # Repopulate the table with filtered results
            self.populate_table()
            
            # Restore original list
            self.teachers = original_teachers
        except Exception as e:
            print(f"Error in search_teachers: {e}")
            # Reset to original data
            self.populate_table()
    
    def show_message(self, title, message):
        """Show a message dialog"""
        messagebox.showinfo(title, message)
    
    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Update status first
            self.status_label.configure(text="Loading teachers data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Get the data
            self.teachers = self.teacher_repo.get_all()
            
            # Update UI
            self.populate_table()
            self.count_label.configure(text=f"Total teachers: {len(self.teachers)}")
            
            # Update status
            self.status_label.configure(text="Teachers tab activated", text_color="#4CC9F0")
            self.after(3000, lambda: self.status_label.configure(
                text="Teachers Component Ready",
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
                print("Unsubscribed from teachers updates")
            except Exception as e:
                print(f"Error unsubscribing from updates: {e}")
    
    def add_sample_data(self):
        """Add sample data to database if it's empty"""
        for teacher in self.teachers:
            self.teacher_repo.add(teacher)
    
    def setup_data_listener(self):
        """Setup real-time data listener for teachers"""
        try:
            self.unsubscribe_function = self.teacher_repo.subscribe_to_changes(self.handle_data_update)
        except Exception as e:
            print(f"Error setting up data listener: {e}")
    
    def handle_data_update(self, updated_teachers):
        """Handle real-time updates from Firebase"""
        try:
            # Store the updated data
            self.teachers = updated_teachers if updated_teachers else []
            
            # Schedule UI updates on the main thread
            self.after(100, self._update_ui_after_data_change)
        except Exception as e:
            print(f"Error in handle_data_update: {e}")
    
    def _update_ui_after_data_change(self):
        """Update UI elements on the main thread"""
        try:
            # Update the UI with the new data
            self.populate_table()
            self.count_label.configure(text=f"Total teachers: {len(self.teachers)}")
            self.show_update_notification()
        except Exception as e:
            print(f"Error updating UI after data change: {e}")
    
    def show_update_notification(self):
        """Show a temporary update notification"""
        self.status_label.configure(text="📡 Data updated in real-time", text_color="#4CC9F0")
        self.after(3000, lambda: self.status_label.configure(
            text="Teachers Component Ready",
            text_color="#4CC9F0"
        )) 