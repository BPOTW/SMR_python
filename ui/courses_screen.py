import tkinter as tk
import customtkinter as ctk
from ui.base_screen import BaseScreen
from ui.custom_functions import CustomFunctions
import tkinter.messagebox as messagebox
from db.course_repository import CourseRepository

class CoursesScreen(BaseScreen):
    """
    Screen for managing course records
    """
    
    def __init__(self, parent, controller):
        BaseScreen.__init__(self, parent, controller)
        
        # Sample course data
        self.courses = [
            {"id": "C001", "name": "Mathematics 101", "teacher": "Dr. Robert Miller", "students": 30, "status": "Active"},
            {"id": "C002", "name": "Science Fundamentals", "teacher": "Dr. Jennifer Lee", "students": 25, "status": "Active"},
            {"id": "C003", "name": "World History", "teacher": "Prof. David Clark", "students": 22, "status": "Inactive"},
            {"id": "C004", "name": "English Literature", "teacher": "Ms. Amanda White", "students": 28, "status": "Active"},
            {"id": "C005", "name": "Advanced Physics", "teacher": "Mr. James Thompson", "students": 15, "status": "Active"}
        ]
        
        # Create header
        self.header = self.create_header("Course Management")
        
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
            "Add Course",
            self.add_course,
            width=150
        )
        self.add_button.pack(side="left", padx=10)
        
        self.edit_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Edit Selected",
            self.edit_course,
            width=150,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=10)
        
        self.delete_button = CustomFunctions.create_custom_button(
            self.action_bar,
            "Delete Selected",
            self.delete_course,
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
            placeholder_text="Search courses...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = CustomFunctions.create_custom_button(
            self.search_frame,
            "Search",
            self.search_courses,
            width=100
        )
        self.search_button.pack(side="left")
        
        # Courses table
        self.table_frame = ctk.CTkFrame(self.content)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers
        columns = ["ID", "Course Name", "Teacher", "Students", "Status", "Actions"]
        widths = [80, 220, 180, 80, 80, 150]
        
        self.table_header = CustomFunctions.create_table_header(
            self.table_frame,
            columns,
            widths
        )
        
        # Create scrollable frame for table rows
        self.table_container = ctk.CTkScrollableFrame(self.table_frame)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Populate table with course data
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with course data"""
        try:
            # Clear existing rows
            for widget in self.table_container.winfo_children():
                widget.destroy()
            
            # Add rows for each course
            for i, course in enumerate(self.courses):
                print(f"Processing course: {course}")
                row_color = "#F8F9FA" if i % 2 == 0 else "#FFFFFF"
                row_frame = ctk.CTkFrame(self.table_container, fg_color=row_color)
                row_frame.pack(fill="x", pady=1)
                
                # Course ID
                id_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("id", "N/A"),
                    width=80
                )
                id_label.pack(side="left", padx=5, pady=10)
                
                # Course Name
                name_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("name", "Unknown"),
                    width=220,
                    anchor="w"
                )
                name_label.pack(side="left", padx=5, pady=10)
                
                # Teacher
                teacher_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("teacher", "N/A"),
                    width=180,
                    anchor="w"
                )
                teacher_label.pack(side="left", padx=5, pady=10)
                
                # Students
                students_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("students", "0"),
                    width=80
                )
                students_label.pack(side="left", padx=5, pady=10)
                
                # Status
                status = course.get("status", "Inactive")
                status_color = "#4CC9F0" if status == "Active" else "#F72585"
                status_label = ctk.CTkLabel(
                    row_frame,
                    text=status,
                    width=80,
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
                    command=lambda c=course: self.view_course(c)
                )
                view_btn.pack(side="left", padx=5)
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    action_frame,
                    text="Edit",
                    width=70,
                    height=25,
                    font=ctk.CTkFont(size=12),
                    command=lambda c=course: self.edit_course(c)
                )
                edit_btn.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error in populate_table: {e}")
            messagebox.showerror("Error", f"Failed to populate courses table: {e}")
    
    def add_course(self):
        """Add a new course"""
        self.show_message("Add Course", "This feature will be implemented in a future update.")
    
    def edit_course(self, course=None):
        """Edit a course record"""
        if course:
            self.show_message("Edit Course", f"Editing {course['name']}")
        else:
            self.show_message("Edit Course", "Please select a course to edit.")
    
    def delete_course(self):
        """Delete a course record"""
        self.show_message("Delete Course", "This feature will be implemented in a future update.")
    
    def view_course(self, course):
        """View a course's details"""
        self.show_message("Course Details", f"Viewing details for {course['name']}")
    
    def search_courses(self):
        """Search for courses"""
        try:
            search_term = self.search_entry.get().lower()
            if not search_term:
                # If search is empty, show all courses
                self.populate_table()
                return
            
            # Filter courses based on search term
            filtered_courses = []
            
            for course in self.courses:
                if isinstance(course, dict):
                    # Use get with default values to avoid KeyError
                    if (search_term in course.get("name", "").lower() or
                        search_term in course.get("id", "").lower() or
                        search_term in course.get("teacher", "").lower() or
                        search_term in str(course.get("students", "")).lower() or
                        search_term in course.get("status", "").lower()):
                        filtered_courses.append(course)
            
            # Update courses list temporarily for display
            original_courses = self.courses
            self.courses = filtered_courses
            
            # Repopulate the table with filtered results
            self.populate_table()
            
            # Restore original list
            self.courses = original_courses
        except Exception as e:
            print(f"Error in search_courses: {e}")
            # Reset to original data
            self.populate_table()
    
    def back_to_dashboard(self):
        """Navigate back to the admin dashboard"""
        self.controller.show_admin() 

    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Update status first
            self.status_label.configure(text="Loading courses data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Get the data
            self.courses = self.course_repo.get_all()
            
            # Update UI
            self.populate_table()
            self.count_label.configure(text=f"Total courses: {len(self.courses)}")
            
            # Update status
            self.status_label.configure(text="Courses data loaded", text_color="#4CC9F0")
            self.after(3000, lambda: self.status_label.configure(
                text="📡 Real-time updates enabled",
                text_color="#4CC9F0"
            ))
        except Exception as e:
            print(f"Error loading tab data: {e}")
            self.status_label.configure(text="Error loading data", text_color="#E76F51")

class CoursesComponent(ctk.CTkFrame):
    """
    Component for managing course records - designed to be embedded in a tabbed interface
    """
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # Initialize the course repository
        self.course_repo = CourseRepository()
        
        # Get courses from database
        self.courses = self.course_repo.get_all()
        print(f"Courses from database: {self.courses}")
        
        # If the database is empty, use sample data
        if not self.courses:
            print("No courses found, using sample data")
            self.courses = [
                {"id": "C001", "name": "Mathematics 101", "teacher": "Dr. Robert Miller", "students": 30, "status": "Active"},
                {"id": "C002", "name": "Science Fundamentals", "teacher": "Dr. Jennifer Lee", "students": 25, "status": "Active"},
                {"id": "C003", "name": "World History", "teacher": "Prof. David Clark", "students": 22, "status": "Inactive"},
                {"id": "C004", "name": "English Literature", "teacher": "Ms. Amanda White", "students": 28, "status": "Active"},
                {"id": "C005", "name": "Advanced Physics", "teacher": "Mr. James Thompson", "students": 15, "status": "Active"}
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
            "Add Course",
            self.add_course,
            width=150
        )
        self.add_button.pack(side="left", padx=10)
        
        # Search bar
        self.search_frame = ctk.CTkFrame(self.action_bar)
        self.search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search courses...",
            width=200
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = CustomFunctions.create_custom_button(
            self.search_frame,
            "Search",
            self.search_courses,
            width=100
        )
        self.search_button.pack(side="left")
        
        # Courses table
        self.table_frame = ctk.CTkFrame(self.content)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table headers
        columns = ["ID", "Course Name", "Teacher", "Students", "Status", "Actions"]
        widths = [80, 220, 180, 80, 80, 150]
        
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
        
        # Total courses count
        self.count_label = ctk.CTkLabel(
            self.status_frame,
            text=f"Total courses: {len(self.courses)}",
            font=ctk.CTkFont(size=12)
        )
        self.count_label.pack(side="left", padx=10, pady=5)
        
        # Populate table with course data
        self.populate_table()
        
        # Setup real-time updates
        self.setup_data_listener()
    
    def add_sample_data(self):
        """Add sample data to database if it's empty"""
        for course in self.courses:
            self.course_repo.add(course)
    
    def setup_data_listener(self):
        """Setup real-time data listener for courses"""
        try:
            self.unsubscribe_function = self.course_repo.subscribe_to_changes(self.handle_data_update)
        except Exception as e:
            print(f"Error setting up data listener: {e}")
    
    def handle_data_update(self, updated_courses):
        """Handle real-time updates from Firebase"""
        try:
            # Store the updated data
            self.courses = updated_courses if updated_courses else []
            
            # Schedule UI updates on the main thread
            self.after(100, self._update_ui_after_data_change)
        except Exception as e:
            print(f"Error in handle_data_update: {e}")
    
    def _update_ui_after_data_change(self):
        """Update UI elements on the main thread"""
        try:
            # Update the UI with the new data
            self.populate_table()
            self.count_label.configure(text=f"Total courses: {len(self.courses)}")
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
        """Populate the table with course data"""
        try:
            # Clear existing rows
            for widget in self.table_container.winfo_children():
                widget.destroy()
            
            # Add rows for each course
            for i, course in enumerate(self.courses):
                print(f"Processing course: {course}")
                row_color = "#F8F9FA" if i % 2 == 0 else "#FFFFFF"
                row_frame = ctk.CTkFrame(self.table_container, fg_color=row_color)
                row_frame.pack(fill="x", pady=1)
                
                # Course ID
                id_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("id", "N/A"),
                    width=80
                )
                id_label.pack(side="left", padx=5, pady=10)
                
                # Course Name
                name_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("name", "Unknown"),
                    width=220,
                    anchor="w"
                )
                name_label.pack(side="left", padx=5, pady=10)
                
                # Teacher
                teacher_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("teacher", "N/A"),
                    width=180,
                    anchor="w"
                )
                teacher_label.pack(side="left", padx=5, pady=10)
                
                # Students
                students_label = ctk.CTkLabel(
                    row_frame,
                    text=course.get("students", "0"),
                    width=80
                )
                students_label.pack(side="left", padx=5, pady=10)
                
                # Status
                status = course.get("status", "Inactive")
                status_color = "#4CC9F0" if status == "Active" else "#F72585"
                status_label = ctk.CTkLabel(
                    row_frame,
                    text=status,
                    width=80,
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
                    command=lambda c=course: self.view_course(c)
                )
                view_btn.pack(side="left", padx=5)
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    action_frame,
                    text="Edit",
                    width=70,
                    height=25,
                    font=ctk.CTkFont(size=12),
                    command=lambda c=course: self.edit_course(c)
                )
                edit_btn.pack(side="left", padx=5)
        except Exception as e:
            print(f"Error in populate_table: {e}")
            messagebox.showerror("Error", f"Failed to populate courses table: {e}")
    
    def add_course(self):
        """Add a new course"""
        self.show_message("Add Course", "This feature will be implemented in a future update.")
    
    def edit_course(self, course=None):
        """Edit a course record"""
        if course:
            self.show_message("Edit Course", f"Editing {course['name']}")
        else:
            self.show_message("Edit Course", "Please select a course to edit.")
    
    def delete_course(self):
        """Delete a course record"""
        self.show_message("Delete Course", "This feature will be implemented in a future update.")
    
    def view_course(self, course):
        """View a course's details"""
        self.show_message("Course Details", f"Viewing details for {course['name']}")
    
    def search_courses(self):
        """Search for courses"""
        try:
            search_term = self.search_entry.get().lower()
            if not search_term:
                # If search is empty, show all courses
                self.populate_table()
                return
            
            # Filter courses based on search term
            filtered_courses = []
            
            for course in self.courses:
                if isinstance(course, dict):
                    # Use get with default values to avoid KeyError
                    if (search_term in course.get("name", "").lower() or
                        search_term in course.get("id", "").lower() or
                        search_term in course.get("teacher", "").lower() or
                        search_term in str(course.get("students", "")).lower() or
                        search_term in course.get("status", "").lower()):
                        filtered_courses.append(course)
            
            # Update courses list temporarily for display
            original_courses = self.courses
            self.courses = filtered_courses
            
            # Repopulate the table with filtered results
            self.populate_table()
            
            # Restore original list
            self.courses = original_courses
        except Exception as e:
            print(f"Error in search_courses: {e}")
            # Reset to original data
            self.populate_table()
    
    def show_message(self, title, message):
        """Show a message dialog"""
        messagebox.showinfo(title, message)
    
    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Update status first
            self.status_label.configure(text="Loading courses data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Get the data
            self.courses = self.course_repo.get_all()
            
            # Update UI
            self.populate_table()
            self.count_label.configure(text=f"Total courses: {len(self.courses)}")
            
            # Update status
            self.status_label.configure(text="Courses data loaded", text_color="#4CC9F0")
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
                print("Unsubscribed from courses updates")
            except Exception as e:
                print(f"Error unsubscribing from updates: {e}") 