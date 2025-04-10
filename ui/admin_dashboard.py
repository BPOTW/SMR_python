import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from db.database_utils import DatabaseUtils
from ui.students_screen import StudentsComponent
from ui.teachers_screen import TeachersComponent
from ui.courses_screen import CoursesComponent
from ui.results_screen import ResultsComponent

class AdminDashboard(ctk.CTkFrame):
    # Custom variables and colors
    students_count = 0
    teachers_count = 0
    courses_count = 0
    results_count = 0
    
    # Color scheme
    SIDEBAR_COLOR = "#1a1c20"  # Dark background
    MAIN_BG_COLOR = "#13151a"  # Darker background for main content
    CARD_COLOR = "#2d2f35"     # Slightly lighter for cards
    ACCENT_COLOR = "#3B8ED0"   # Primary accent color
    ACCENT_HOVER = "#1F6AA5"   # Darker accent for hover
    SUCCESS_COLOR = "#4CC9F0"  # Success/info color
    WARNING_COLOR = "#FFBE0B"  # Warning color
    DANGER_COLOR = "#E76F51"   # Danger/error color
    TEXT_COLOR = "#ffffff"     # Main text color
    SECONDARY_TEXT = "#94969c"  # Secondary text color

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent, fg_color=self.MAIN_BG_COLOR)
        self.controller = controller
        
        # Initialize current tab
        self.current_tab = 0
        
        # Initialize data loading
        self.load_initial_data()
        
        # Setup real-time data listener
        self.setup_data_listener()
        
        # Create sidebar for navigation
        self.create_sidebar()
        
        # Setup tabs
        self.setup_tabs()
    
    def create_sidebar(self):
        # Create sidebar for navigation
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#1a1c20")
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        self.title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.title_frame.pack(fill="x", padx=20, pady=(20, 30))
        
        self.logo_label = ctk.CTkLabel(
            self.title_frame, 
            text="SMR\nDashboard", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CC9F0"
        )
        self.logo_label.pack(pady=(10, 5))
        
        # Navigation links
        self.nav_items = [
            {"text": "Dashboard", "index": 0},
            {"text": "Results", "index": 1},
            {"text": "Analytics", "index": 2},
            {"text": "Students", "index": 3},
            {"text": "Teachers", "index": 4},
            {"text": "Courses", "index": 5},
            {"text": "Settings", "index": 6},
        ]
        
        # Add navigation buttons
        self.nav_buttons = []
        
        for item in self.nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f" {item['text']}",
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#2d2f35",
                anchor="w",
                command=lambda i=item["index"]: self.show_tab(i)
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_buttons.append(btn)
            
        # Update selected button style
        self.highlight_selected_tab()

    def setup_tabs(self):
        """Set up the main content area with frames for each tab"""
        # Create main content container
        self.main_content = ctk.CTkFrame(self, fg_color="#2d2f35")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Create frames for each tab
        self.tabs = []
        
        # Dashboard Tab
        dashboard_frame = self.create_dashboard_tab()
        self.tabs.append(dashboard_frame)
        
        # Results Tab
        results_frame = ResultsComponent(self.main_content, self)
        self.tabs.append(results_frame)

        # Analytics Tab
        analytics_frame = self.create_placeholder_tab("Analytics")
        self.tabs.append(analytics_frame)
        
        # Students Tab
        students_frame = StudentsComponent(self.main_content, self)
        self.tabs.append(students_frame)
        
        # Teachers Tab
        teachers_frame = TeachersComponent(self.main_content, self)
        self.tabs.append(teachers_frame)
        
        # Courses Tab
        courses_frame = CoursesComponent(self.main_content, self)
        self.tabs.append(courses_frame)
        
        
        
        # Settings Tab
        settings_frame = self.create_placeholder_tab("Settings")
        self.tabs.append(settings_frame)
        
        # Show default tab (Dashboard)
        self.show_tab(0)
    
    def load_initial_data(self):
        """Load initial data from Firebase"""
        try:
            # Get counts from main_data collection
            document = DatabaseUtils.get_document_by_id("main_data", "count_data")
            if document:
                self.update_counts(document)
                print("Initial data loaded successfully")
            else:
                print("Count data document not found")
                self.create_initial_count_data()
        except Exception as e:
            print(f"Error loading initial data: {e}")
            messagebox.showerror("Error", "Failed to load initial data")

    def create_initial_count_data(self):
        """Create initial count data if it doesn't exist"""
        try:
            # Get actual counts from collections
            students = DatabaseUtils.get_collection_data("students")
            teachers = DatabaseUtils.get_collection_data("teachers")
            courses = DatabaseUtils.get_collection_data("courses")
            
            # Create count data document
            count_data = {
                'students_count': len(students) if students else 0,
                'teachers_count': len(teachers) if teachers else 0,
                'courses_count': len(courses) if courses else 0,
                'results_count': 0  # Initialize to 0
            }
            
            # Add document to Firebase
            DatabaseUtils.add_document("main_data", "count_data", count_data)
            self.update_counts(count_data)
            print("Initial count data created")
        except Exception as e:
            print(f"Error creating initial count data: {e}")

    def setup_data_listener(self):
        """Setup real-time data listeners for all collections"""
        try:
            # Listen for changes in main_data collection
            self.count_unsubscribe = DatabaseUtils.watch_collection(
                "main_data",
                self.handle_count_update
            )
            
            # Listen for changes in individual collections
            self.students_unsubscribe = DatabaseUtils.watch_collection(
                "students",
                self.handle_students_update
            )
            
            self.teachers_unsubscribe = DatabaseUtils.watch_collection(
                "teachers",
                self.handle_teachers_update
            )
            
            self.courses_unsubscribe = DatabaseUtils.watch_collection(
                "courses",
                self.handle_courses_update
            )
            
            print("Real-time listeners setup successfully")
        except Exception as e:
            print(f"Error setting up data listeners: {e}")

    def update_counts(self, count_data):
        """Update the counts from count_data document"""
        try:
            # Store updated counts
            self.students_count = count_data.get('students_count', 0)
            self.teachers_count = count_data.get('teachers_count', 0)
            self.courses_count = count_data.get('courses_count', 0)
            self.results_count = count_data.get('results_count', 0)
            
            # Schedule UI update on main thread
            if hasattr(self, 'dashboard_frame'):
                self.after(100, self._safe_update_dashboard_ui)
        except Exception as e:
            print(f"Error updating counts: {e}")
    
    def _safe_update_dashboard_ui(self):
        """Safely update dashboard UI on the main thread"""
        try:
            self.update_dashboard_ui()
        except Exception as e:
            print(f"Error in safe dashboard UI update: {e}")

    def update_dashboard_ui(self):
        """Update the dashboard UI with current counts"""
        try:
            # Get the stats frame
            stats_frame = self.dashboard_frame.winfo_children()[1]
            
            # Update each stat card
            stat_data = [
                ("Students", self.students_count),
                ("Teachers", self.teachers_count),
                ("Courses", self.courses_count),
                ("Results Pending", self.results_count)
            ]
            
            for i, (title, count) in enumerate(stat_data):
                card = stats_frame.grid_slaves(row=0, column=i)[0]
                count_label = card.winfo_children()[1]  # Count label is the second child
                count_label.configure(text=str(count))
                
        except Exception as e:
            print(f"Error updating dashboard UI: {e}")

    def handle_count_update(self, data):
        """Handle updates to the count_data document"""
        try:
            if data and len(data) > 0:
                # Schedule the update on the main thread
                count_data = data[0]
                self.after(100, lambda: self.update_counts(count_data))
        except Exception as e:
            print(f"Error in handle_count_update: {e}")
            
    def handle_students_update(self, data):
        """Handle updates to the students collection"""
        try:
            # Schedule database update on main thread to avoid threading issues
            self.after(100, lambda: self._update_students_count(data))
        except Exception as e:
            print(f"Error handling students update: {e}")
    
    def _update_students_count(self, data):
        """Update students count in database (called on main thread)"""
        try:
            # Update students count in main_data
            DatabaseUtils.update_document("main_data", "count_data", {
                'students_count': len(data) if data else 0
            })
        except Exception as e:
            print(f"Error updating students count: {e}")

    def handle_teachers_update(self, data):
        """Handle updates to the teachers collection"""
        try:
            # Schedule database update on main thread to avoid threading issues
            self.after(100, lambda: self._update_teachers_count(data))
        except Exception as e:
            print(f"Error handling teachers update: {e}")
    
    def _update_teachers_count(self, data):
        """Update teachers count in database (called on main thread)"""
        try:
            # Update teachers count in main_data
            DatabaseUtils.update_document("main_data", "count_data", {
                'teachers_count': len(data) if data else 0
            })
        except Exception as e:
            print(f"Error updating teachers count: {e}")

    def handle_courses_update(self, data):
        """Handle updates to the courses collection"""
        try:
            # Schedule database update on main thread to avoid threading issues
            self.after(100, lambda: self._update_courses_count(data))
        except Exception as e:
            print(f"Error handling courses update: {e}")
    
    def _update_courses_count(self, data):
        """Update courses count in database (called on main thread)"""
        try:
            # Update courses count in main_data
            DatabaseUtils.update_document("main_data", "count_data", {
                'courses_count': len(data) if data else 0
            })
        except Exception as e:
            print(f"Error updating courses count: {e}")
    
    def cleanup(self):
        """Clean up resources when the dashboard is destroyed"""
        try:
            # Unsubscribe from all data listeners
            if hasattr(self, 'count_unsubscribe') and self.count_unsubscribe:
                self.count_unsubscribe()
            if hasattr(self, 'students_unsubscribe') and self.students_unsubscribe:
                self.students_unsubscribe()
            if hasattr(self, 'teachers_unsubscribe') and self.teachers_unsubscribe:
                self.teachers_unsubscribe()
            if hasattr(self, 'courses_unsubscribe') and self.courses_unsubscribe:
                self.courses_unsubscribe()
            
            if hasattr(self, 'students_component'):
                self.students_component.cleanup()
            if hasattr(self, 'teachers_component'):
                self.teachers_component.cleanup()
            if hasattr(self, 'courses_component'):
                self.courses_component.cleanup()
            if hasattr(self, 'results_component'):
                self.results_component.cleanup()
                
            print("Cleaned up all listeners")
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        super().destroy()
        print("AdminDashboard destroyed")

    def show_tab(self, index):
        """Show the selected tab and hide others"""
        for i, tab in enumerate(self.tabs):
            if i == index:
                tab.pack(fill="both", expand=True)
                # Call on_tab_selected if the method exists
                if hasattr(tab, 'on_tab_selected'):
                    tab.on_tab_selected()
            else:
                tab.pack_forget()
        
        # Update the selected tab indicator
        self.current_tab = index
        self.highlight_selected_tab()

    def create_dashboard_tab(self):
        """Create the dashboard tab content"""
        # Create main frame for dashboard
        self.dashboard_frame = ctk.CTkFrame(self.main_content, fg_color="#13151a")
        
        # Welcome header
        header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        welcome_title = ctk.CTkLabel(
            header_frame,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        welcome_title.pack(anchor="w")
        
        welcome_desc = ctk.CTkLabel(
            header_frame,
            text="Welcome to the Smart Result System Admin Dashboard",
            font=ctk.CTkFont(size=14),
            text_color="#94969c"
        )
        welcome_desc.pack(anchor="w", pady=(0, 10))
        
        # Statistics cards
        stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Create 4 statistic cards in a grid
        stats = [
            {"title": "Students", "count": self.students_count, "icon": "👨‍🎓"},
            {"title": "Teachers", "count": self.teachers_count, "icon": "👨‍🏫"},
            {"title": "Courses", "count": self.courses_count, "icon": "📚"},
            {"title": "Results Pending", "count": self.results_count, "icon": "📊"}
        ]
        
        for i, stat in enumerate(stats):
            # Create card
            card = ctk.CTkFrame(stats_frame, fg_color="#2d2f35", corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            # Add icon and title
            icon_label = ctk.CTkLabel(
                card,
                text=stat["icon"],
                font=ctk.CTkFont(size=32),
                text_color="#4CC9F0"
            )
            icon_label.pack(pady=(15, 5))
            
            # Add count
            count_label = ctk.CTkLabel(
                card,
                text=str(stat["count"]),
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color="#ffffff"
            )
            count_label.pack(pady=5)
            
            # Add title
            title_label = ctk.CTkLabel(
                card,
                text=stat["title"],
                font=ctk.CTkFont(size=14),
                text_color="#94969c"
            )
            title_label.pack(pady=(0, 15))
            
            # Make cards equal width
            card.configure(width=160, height=140)
        
        # Configure grid weights
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)
        
        # Recent activity section
        activity_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#2d2f35", corner_radius=10)
        activity_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Activity header
        activity_title = ctk.CTkLabel(
            activity_frame,
            text="Recent Activity",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        activity_title.pack(anchor="w", padx=20, pady=(20, 5))
        
        activity_desc = ctk.CTkLabel(
            activity_frame,
            text="Manage students, teachers, courses and results from the dashboard",
            font=ctk.CTkFont(size=12),
            text_color="#94969c"
        )
        activity_desc.pack(anchor="w", padx=20, pady=(0, 20))
        
        return self.dashboard_frame
    
    def create_placeholder_tab(self, title):
        """Create a placeholder tab with a message"""
        frame = ctk.CTkFrame(self.main_content, fg_color="#13151a")
        
        # Center content
        center_frame = ctk.CTkFrame(frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon
        icon_label = ctk.CTkLabel(
            center_frame,
            text="🚧",
            font=ctk.CTkFont(size=64),
            text_color="#FFBE0B"
        )
        icon_label.pack(pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            center_frame,
            text=f"{title} Coming Soon",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=10)
        
        # Description
        desc_label = ctk.CTkLabel(
            center_frame,
            text=f"The {title} section is under development and will be available soon.",
            font=ctk.CTkFont(size=14),
            text_color="#94969c"
        )
        desc_label.pack(pady=5)
        
        return frame
    
    def highlight_selected_tab(self):
        """Highlight the currently selected tab in the sidebar"""
        # Reset all button styles
        for i, btn in enumerate(self.nav_buttons):
            if i == self.current_tab:
                # Highlight selected button
                btn.configure(
                    fg_color=self.ACCENT_COLOR,
                    text_color="#ffffff",
                    hover_color=self.ACCENT_HOVER
                )
            else:
                # Reset other buttons
                btn.configure(
                    fg_color="transparent",
                    text_color="#ffffff",
                    hover_color="#2d2f35"
                ) 