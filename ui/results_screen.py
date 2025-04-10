import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from ui.base_screen import BaseScreen
from ui.custom_functions import CustomFunctions
from db.database_utils import DatabaseUtils
from db.data_access import results_data, students_data, courses_data, teachers_data
import utils.result_helpers as result_helpers
import utils.pdf_generator as pdf_generator
import os

class ResultsComponent(ctk.CTkFrame):
    """
    Component for managing student results - designed to be embedded in a tabbed interface
    """
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # Initialize data with sample results
        self.results = [
            {
                "id": "R001",
                "class_incharge": "John Smith",
                "class": "11",
                "status": {},
                "action": "View",
            },
        ]

        # Create loading indicator (initially hidden)
        self.loading_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.progress_bar = ctk.CTkProgressBar(self.loading_frame, mode="indeterminate", width=120)
        self.progress_bar.pack(pady=10)
        
        self.loading_label = ctk.CTkLabel(
            self.loading_frame, 
            text="Loading data...", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4CC9F0"
        )
        self.loading_label.pack()
        
        # Hide loading indicator initially
        self.loading_frame.place_forget()

        # Create main content area with dark theme
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Create action buttons
        self.action_bar = ctk.CTkFrame(self.content, fg_color="transparent")
        self.action_bar.pack(fill="x", padx=10, pady=10)
        
        self.add_button = ctk.CTkButton(
            self.action_bar,
            text="+ Create Result",
            command=self.add_result_entry,
            width=150,
            fg_color="#3B8ED0",
            hover_color="#1F6AA5"
        )
        self.add_button.pack(side="left", padx=10)
        
        # Add demo button for testing
        self.demo_button = ctk.CTkButton(
            self.action_bar,
            text="Add Demo Result",
            command=self.add_demo_result,
            width=150,
            fg_color="#7209B7",
            hover_color="#480CA8"
        )
        self.demo_button.pack(side="left", padx=10)
        
        # Filter options
        self.filter_frame = ctk.CTkFrame(self.action_bar, fg_color="#2d2f35")
        self.filter_frame.pack(side="right", padx=10)
        
        # Class filter
        self.class_var = tk.StringVar(value="All Classes")
        self.class_filter = ctk.CTkOptionMenu(
            self.filter_frame,
            variable=self.class_var,
            values=["All Classes", "11", "12"],
            command=self.apply_filters,
            width=120,
            fg_color="#2d2f35",
            button_color="#3B8ED0",
            button_hover_color="#1F6AA5"
        )
        self.class_filter.pack(side="left", padx=5)
        
        # Subject filter
        self.subject_var = tk.StringVar(value="All Results")
        self.subject_filter = ctk.CTkOptionMenu(
            self.filter_frame,
            variable=self.subject_var,
            values=["All Results", "Pending", "Ready"],
            command=self.apply_filters,
            width=120,
            fg_color="#2d2f35",
            button_color="#3B8ED0",
            button_hover_color="#1F6AA5"
        )
        self.subject_filter.pack(side="left", padx=5)
        
        # Search bar
        self.search_frame = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        self.search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search results...",
            width=200,
            fg_color="#2d2f35",
            border_color="#3B8ED0",
            text_color="#ffffff"
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self.search_results,
            width=100,
            fg_color="#3B8ED0",
            hover_color="#1F6AA5"
        )
        self.search_button.pack(side="left")

        # Status indicator frame at the bottom
        self.status_frame = ctk.CTkFrame(self.content, height=30, fg_color="#2d2f35")
        self.status_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="📊 Results Component Ready",
            font=ctk.CTkFont(size=12),
            text_color="#4CC9F0"
        )
        self.status_label.pack(side="right", padx=10, pady=5)
        
        # Total results count
        self.count_label = ctk.CTkLabel(
            self.status_frame,
            text=f"Total results: {len(self.results)}",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff"
        )
        self.count_label.pack(side="left", padx=10, pady=5)

        self.table_frame = ctk.CTkFrame(self.content, fg_color="#2d2f35")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["ID", "Class", "Class Incharge", "Status", "Action"]
        widths = [240, 80, 200, 150, 250]
        
        # Create header with dark theme
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#1a1c20")
        header_frame.pack(fill="x", padx=5, pady=(10, 0))
        
        for col, width in zip(columns, widths):
            header_label = ctk.CTkLabel(
                header_frame,
                text=col,
                width=width,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff"
            )
            header_label.pack(side="left", padx=5, pady=10)
        
        # Create scrollable frame for table rows
        self.table_container = ctk.CTkScrollableFrame(
            self.table_frame,
            fg_color="#2d2f35"
        )
        self.table_container.pack(fill="both", expand=True, padx=0, pady=10)
        
        # Populate table with result data
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with result data"""
        # Clear existing data
        for item in self.table_container.winfo_children():
            item.destroy()
        
        # Add results to table
        for i, result in enumerate(self.results):
            row = ctk.CTkFrame(self.table_container, fg_color="#1a1c20" if i % 2 == 0 else "#2d2f35")
            row.pack(fill="x", pady=1)

            
            # Check if one of the subjects is pending
            all_pending = "Ready"
            # print(f"Printing result data in popuate : {result}")
            if 'pending' in [status.lower() for status in result['status'].values()]:
                    all_pending = "Pending"
            # print(f"Printing all pending : {all_pending}")
            # Add result data
            ctk.CTkLabel(row, text=result.get('id', 'N/A'), width=240, text_color="#ffffff").pack(side="left", padx=5, pady=10)
            ctk.CTkLabel(row, text=str(result.get('class', 'N/A')), width=80, text_color="#ffffff").pack(side="left", padx=5, pady=10)
            ctk.CTkLabel(row, text=result.get('class_incharge', 'N/A'), width=200, text_color="#ffffff").pack(side="left", padx=5, pady=10)
            ctk.CTkLabel(row, text=all_pending, width=150, text_color="#ffffff").pack(side="left", padx=5, pady=10)
            
            # Actions frame
            actions_frame = ctk.CTkFrame(row, fg_color="transparent", width=250)
            actions_frame.pack(side="left", fill="x")
            
            # View button
            view_btn = ctk.CTkButton(
                actions_frame,
                text="Info",
                width=60,
                height=24,
                fg_color="#3B8ED0",
                hover_color="#1F6AA5",
                command=lambda r=result: self.view_result(r)
            )
            view_btn.pack(side="left", padx=2)
            
            # Edit button
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Edit",
                width=60,
                height=24,
                fg_color="#3B8ED0",
                hover_color="#1F6AA5",
                command=lambda r=result: self.edit_result(r)
            )
            edit_btn.pack(side="left", padx=2)

            # Create Result button
            create_btn = ctk.CTkButton(
                actions_frame,
                text="Create PDF",
                width=75,
                height=24,
                fg_color="#3B8ED0",
                hover_color="#1F6AA5",
                command=lambda r=result, status=all_pending: self.create_pdf(r, status)
            )
            create_btn.pack(side="left", padx=2)

            # Create Result button
            create_btn = ctk.CTkButton(
                actions_frame,
                text="Send",
                width=55,
                height=24,
                fg_color="#3B8ED0",
                hover_color="#1F6AA5",
                command=lambda r=result, status=all_pending: self.create_result(r, status)
            )
            create_btn.pack(side="left", padx=2)

            # Create Print button
            create_btn = ctk.CTkButton(
                actions_frame,
                text="Print",
                width=65,
                height=24,
                fg_color="#3B8ED0",
                hover_color="#1F6AA5",
                command=lambda r=result, status=all_pending: self.print_result()
            )
            create_btn.pack(side="left", padx=2)
  
    def get_grade_color(self, grade):
        """Return color based on grade"""
        grade_colors = {
            'A+': '#4CC9F0',  # Bright blue
            'A': '#4895EF',   # Blue
            'A-': '#4361EE',  # Darker blue
            'B+': '#3F37C9',  # Purple-blue
            'B': '#3A0CA3',   # Purple
            'B-': '#480CA8',  # Darker purple
            'C+': '#7209B7',  # Pink-purple
            'C': '#B5179E',   # Pink
            'F': '#F72585'    # Red
        }
        return grade_colors.get(grade, '#ffffff')  # Default to white if grade not found
    
    def add_result_entry(self):
        """Show dialog to add a new result entry"""

        # Get data from database
        main_data = DatabaseUtils.get_document_by_id("main_data", "app_data")
        # Get class incharges from database
        class_incharges = DatabaseUtils.get_document_by_id("main_data", "class_incharges")
        
        # Create dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create New Result")
        dialog.geometry("450x700")  # Increased height for subject entries
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.attributes("-topmost", True)
        
        # Add padding frame
        content_frame = ctk.CTkFrame(dialog, fg_color="#2d2f35")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="Create New Result",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(0, 20))
        
        # Form fields
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Class field
        class_label = ctk.CTkLabel(
            form_frame, 
            text="Class:",
            font=ctk.CTkFont(weight="bold"),
            text_color="#4CC9F0"
        )
        class_label.grid(row=0, column=0, sticky="e", padx=(0,10), pady=10)
        
        class_var = tk.StringVar()
        # Get classes from database
        class_options = main_data.get('classes', ['11', '12'])  # Fallback to defaults if not found
        class_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=class_var,
            values=class_options,
            width=200,
            fg_color="#1a1c20",
            button_color="#3B8ED0",
        )
        class_dropdown.grid(row=0, column=1, sticky="w", pady=10)
        class_dropdown.set(class_options[0] if class_options else "")
        
        # Section field
        section_label = ctk.CTkLabel(
            form_frame, 
            text="Section:",
            font=ctk.CTkFont(weight="bold"),
            text_color="#4CC9F0"
        )
        section_label.grid(row=1, column=0, sticky="e", padx=(0,10), pady=10)
        
        section_var = tk.StringVar()
        section_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=section_var,
            values=[""],  # Will be populated based on selected class
            width=200,
            fg_color="#1a1c20",
            button_color="#3B8ED0",
        )
        section_dropdown.grid(row=1, column=1, sticky="w", pady=10)

        # Test name field
        test_name_label = ctk.CTkLabel(
            form_frame,
            text="Test Name:",
            font=ctk.CTkFont(weight="bold"),
            text_color="#4CC9F0"
        )
        test_name_label.grid(row=2, column=0, sticky="e", padx=(0,10), pady=10)

        test_name_entry = ctk.CTkEntry(
            form_frame,
            width=200,
            fg_color="#1a1c20",
            border_color="#3B8ED0",)

        test_name_entry.grid(row=2, column=1, sticky="w", pady=10)
        
        # Class Incharge field
        incharge_label = ctk.CTkLabel(
            form_frame, 
            text="Class Incharge:",
            font=ctk.CTkFont(weight="bold"),
            text_color="#4CC9F0"
        )
        incharge_label.grid(row=3, column=0, sticky="e", padx=(0,10), pady=10)
        
        incharge_entry = ctk.CTkEntry(
            form_frame,
            width=200,
            fg_color="#1a1c20",
            border_color="#3B8ED0",
            text_color="#ffffff"
        )
        incharge_entry.grid(row=3, column=1, sticky="w", pady=10)
        
        # Create a scrollable frame for subjects
        subjects_label = ctk.CTkLabel(
            content_frame,
            text="Subjects & Max Marks",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        subjects_label.pack(pady=(20, 5), anchor="w", padx=10)
        
        subjects_frame = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="#1a1c20",
            height=200
        )
        subjects_frame.pack(fill="x", padx=10, pady=5)
        
        # Dictionary to store subject entry widgets
        subject_entries = {}
        
        # Function to update subjects based on class and section
        def update_subjects():
            # Clear existing subjects
            for widget in subjects_frame.winfo_children():
                widget.destroy()
            subject_entries.clear()
            
            current_class = class_var.get()
            current_section = section_var.get()
            
            if not current_class or not current_section:
                return
            
            # Get subjects for this class and section
            try:
                if ('section_subjects' in main_data and 
                    current_class in main_data['section_subjects'] and 
                    current_section in main_data['section_subjects'][current_class]):
                    subjects = main_data['section_subjects'][current_class][current_section]
                else:
                    subjects = []
                    
                # Create entry fields for each subject
                for i, subject in enumerate(subjects):
                    subject_frame = ctk.CTkFrame(subjects_frame, fg_color="transparent")
                    subject_frame.pack(fill="x", padx=5, pady=5)
                    
                    # Subject name
                    subject_label = ctk.CTkLabel(
                        subject_frame,
                        text=subject,
                        font=ctk.CTkFont(weight="bold"),
                        text_color="#4CC9F0",
                        width=150
                    )
                    subject_label.pack(side="left", padx=(10, 10))
                    
                    # Max marks entry
                    max_marks_entry = ctk.CTkEntry(
                        subject_frame,
                        width=100,
                        fg_color="#2d2f35",
                        border_color="#3B8ED0",
                        placeholder_text="Max Marks"
                    )
                    max_marks_entry.pack(side="right", padx=(10, 10))
                    max_marks_entry.insert(0, "100")  # Default value
                    
                    # Store entry widget for later retrieval
                    subject_entries[subject] = max_marks_entry
                
                if not subjects:
                    no_subjects_label = ctk.CTkLabel(
                        subjects_frame, 
                        text="No subjects found for this class and section",
                        text_color="#F72585"
                    )
                    no_subjects_label.pack(pady=20)
            except Exception as e:
                print(f"Error updating subjects: {e}")
                error_label = ctk.CTkLabel(
                    subjects_frame, 
                    text=f"Error loading subjects: {str(e)}",
                    text_color="#F72585"
                )
                error_label.pack(pady=20)
        
        # Update sections when class changes
        def update_sections(*args):
            current_class = class_var.get()
            
            # Clear current section dropdown
            section_dropdown.configure(values=[""])
            section_var.set("")
            
            # Get sections for selected class from database
            if current_class and 'sections' in main_data and current_class in main_data['sections']:
                section_options = main_data['sections'][current_class]
                section_dropdown.configure(values=section_options)
                if section_options:
                    section_var.set(section_options[0])
            
            # Also update teacher after changing class
            update_teacher()
            # Update subjects when class changes
            update_subjects()

        # Update incharge entry when class or section changes
        def update_teacher(*args):
            try:
                # Clear current value
                incharge_entry.delete(0, 'end')
                
                # Get current class and section values
                current_class = class_var.get()
                current_section = section_var.get()
                
                if not current_class or not current_section:
                    incharge_entry.insert(0, "")
                    return
                
                # Update with appropriate incharge from database
                if (current_class in class_incharges and 
                    current_section in class_incharges[current_class]):
                    teacher_name = class_incharges[current_class][current_section]
                    incharge_entry.insert(0, teacher_name)
                else:
                    # Fallback if specific combination not found
                    incharge_entry.insert(0, "No incharge assigned")
            except Exception as e:
                print(f"Error updating incharge: {e}")
                incharge_entry.insert(0, "Error loading incharge")
        
            # Update subjects when section changes
            update_subjects()
        
        # Set up dynamic updates when dropdown values change
        class_var.trace_add("write", update_sections)
        section_var.trace_add("write", update_teacher)
        
        # Initialize sections dropdown based on initial class selection
        update_sections()
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        # Save function
        def save_result():
            class_number = class_var.get()
            section = section_var.get()
            class_incharge = incharge_entry.get()
            test_name = test_name_entry.get()
            
            if not class_number:
                messagebox.showerror("Error", "Please select a class")
                return
                
            if not section:
                messagebox.showerror("Error", "Please select a section")
                return
                
            if not test_name:
                messagebox.showerror("Error", "Please enter a test name")
                return
            
            if not class_incharge or class_incharge == "No incharge assigned":
                messagebox.showerror("Error", "Please enter class incharge name")
                return
            
            # Get subjects
            subjects = list(subject_entries.keys())
            if not subjects:
                messagebox.showerror("Error", "No subjects found for this class and section")
                return
            
            # Create subjects status data
            subjects_data = {}
            for subject in subjects:
                subjects_data[subject] = 'Pending'
            
            # Create max marks data
            max_marks_data = {}
            for subject, entry in subject_entries.items():
                try:
                    marks = int(entry.get())
                    if marks <= 0:
                        messagebox.showerror("Error", f"Max marks for {subject} must be positive")
                        return
                    max_marks_data[subject] = marks
                except ValueError:
                    messagebox.showerror("Error", f"Invalid max marks for {subject}")
                return
            
            try:
                # Create result entry
                result_id = result_helpers.create_result_entry(
                    int(class_number), 
                    section, 
                    class_incharge,
                    test_name,
                    max_marks_data,  # Now passing the max marks dictionary
                    subjects_data
                )
                
                if result_id:
                    # Show success message
                    self.status_label.configure(text="✅ Result entry added!", text_color="#4CC9F0")
                    
                    # Refresh the data
                    self.after(100, self._load_tab_data)
                    
                    # Close dialog
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to create result entry")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#F72585",
            hover_color="#B5179E",
            width=120
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Create Result",
            command=save_result,
            fg_color="#3B8ED0",
            hover_color="#1F6AA5",
            width=120
        )
        save_btn.pack(side="right", padx=10)
        
        # Wait for dialog to close
        self.wait_window(dialog)
    
    def edit_result(self, result):
        """Show dialog to edit a result"""
        messagebox.showinfo("Edit Result", f"Editing result for {result['class']}")
    
    # Create PDF
    def create_pdf(self, result, status):
        if status != "Ready":
            messagebox.showwarning("Cannot Create PDF", "Cannot generate PDF because some subject results are still pending.")
            return

        try:
            # --- Data Extraction ---
            result_id = result.get('id', 'UnknownResult')
            class_num = result.get('class', 'N/A')
            section = result.get('section', 'N/A')
            test_name = result.get('test_name', 'Result Sheet')
            # Extract the new maxMarks dictionary
            max_marks_map = result.get('maxMarks', {}) # Get the map
            if not max_marks_map:
                 messagebox.showwarning("Warning", "Max marks data ('maxMarks') is missing or empty for this result. Total marks might be incorrect.")
                 # Decide if you want to stop or continue with default/zero values

            subjects = list(result.get('status', {}).keys())
            if not subjects:
                 messagebox.showerror("Error", "No subjects found for this result entry.")
                 return

            students_marks_data = result.get('marks', {})
            if not students_marks_data:
                 messagebox.showinfo("Info", "No student marks data found to generate PDF.")
                 return

            # --- PDF Generation ---
            pdf_title = f"{test_name} ({class_num} - {section})"

            # Instantiate the generator passing the max_marks_map
            generator = pdf_generator.ResultSheetGenerator(
                exam_title=pdf_title,
                max_marks_map=max_marks_map # Pass the map here
                # Removed max_marks_per_subject
            )

            # Set subjects (important for order)
            generator.set_subjects(subjects)

            # --- Sort Students (as before) ---
            try:
                sorted_student_items = sorted(
                    students_marks_data.items(),
                    key=lambda item: int(item[0])
                )
            except ValueError:
                 messagebox.showerror("Error", "Could not sort students by roll number. Ensure roll numbers are numeric.")
                 return

            # --- Add Students (as before) ---
            for roll_no, student_data in sorted_student_items:
                student_name = student_data.get('name', 'Unknown Name')
                student_subject_results = student_data.get('result', {})
                marks_in_order = []
                for subj in subjects:
                    marks_in_order.append(student_subject_results.get(subj, 0))
                generator.add_student(roll_no, student_name, *marks_in_order)

            # --- Save and Open PDF (as before) ---
            output_dir = os.path.join(os.path.expanduser("~"), "Documents", "SmartResultSystem")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            pdf_filename = f"Result_{class_num}_{section}_{result_id}.pdf"
            pdf_filepath = os.path.join(output_dir, pdf_filename)

            generated_path = generator.generate_pdf(filepath=pdf_filepath)

            if generated_path:
                messagebox.showinfo("Success", f"PDF generated successfully!\nSaved to: {generated_path}")
                try:
                    os.startfile(generated_path)
                except Exception as e:
                    print(f"Could not auto-open PDF: {e}")
                    messagebox.showwarning("Open PDF", f"Could not automatically open the PDF. Please find it at:\n{generated_path}")
            else:
                messagebox.showerror("Error", "Failed to generate PDF.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during PDF generation: {str(e)}")
            print(f"Error in create_pdf: {e}")
    
    def print_result(self):
        #functionality coming soon
        messagebox.showinfo("Print Result", "Print functionality coming soon")
        # result_path = os.path.join(os.path.expanduser("~"), "Documents", "class_results.pdf")
        # os.startfile(result_path, "print")

    def view_result(self, result):
        """Show dialog box with result details"""

        fields = [
            ("Result ID:", result.get('id', 'N/A')),
            ("Class:", result.get('class', 'N/A')),
            ("Class Incharge:", result.get('class_incharge', 'N/A')),
            # ("Status:", result.get('status', {})),
            # ("English:", result.get('status', {}).get('english', 'N/A')),
        ]

        for subject in result.get('status', {}).keys():
            fields.append((subject, result.get('status', {}).get(subject, 'N/A')))

        # Create dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("View Result Details")
        height = 300 + (len(fields) - 1) * 30
        dialog.geometry(f"500x{height}")
        dialog.resizable(False, False)
        
        # Add padding frame
        content_frame = ctk.CTkFrame(dialog, fg_color="#2d2f35")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            content_frame,
            text="Result Details",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        title.pack(pady=(0, 20))
        
        # Details grid
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill="x", padx=10)
        
        # Field labels and values
        
        for i, (label, value) in enumerate(fields):
            # Label
            ctk.CTkLabel(
                details_frame,
                text=label,
                font=ctk.CTkFont(weight="bold"),
                text_color="#4CC9F0"
            ).grid(row=i, column=0, sticky="e", padx=(0,10), pady=5)
            
            # Value
            ctk.CTkLabel(
                details_frame,
                text=value,
                text_color="#ffffff"
            ).grid(row=i, column=1, sticky="w", pady=5)
        
        # Close button
        close_btn = ctk.CTkButton(
            content_frame,
            text="Close",
            command=dialog.destroy,
            fg_color="#3B8ED0",
            hover_color="#1F6AA5"
        )
        close_btn.pack(pady=20)
        
        # Make dialog modal
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
    
    def apply_filters(self, *args):
        """Apply class and subject filters"""
        selected_class = self.class_var.get()
        selected_status = self.subject_var.get()
        
        print(f"Filtering: Class={selected_class}, Status={selected_status}")

        # Get fresh data
        all_results = results_data.get_all() or []
        
        # Sort by creation date first (latest first)
        all_results.sort(key=lambda x: x.get('created_at', 0), reverse=True)
        
        filtered_results = all_results
        
        # Apply class filter
        if selected_class != "All Classes":
            filtered_results = [r for r in filtered_results if str(r.get('class')) == selected_class]
            print(f"After class filter: {len(filtered_results)} results")
        
        # Apply status filter
        if selected_status != "All Results":
            # Status is a dictionary with multiple values, need to check if any are "pending"
            if selected_status == "Pending":
                filtered_results = [
                    r for r in filtered_results 
                    if "status" in r and isinstance(r["status"], dict) and 
                    "pending" in [status.lower() for status in r["status"].values()]
                ]
            else:  # Ready
                filtered_results = [
                    r for r in filtered_results 
                    if "status" in r and isinstance(r["status"], dict) and 
                    "pending" not in [status.lower() for status in r["status"].values()]
                ]
            print(f"After status filter: {len(filtered_results)} results")
        
        # Display filtered results temporarily
        temp_results = self.results
        self.results = filtered_results
        
        # Update table with filtered data
        self.populate_table()
        self.count_label.configure(text=f"Filtered results: {len(filtered_results)}")
        
        # Restore original dataset (not display)
        self.results = temp_results
    
    def search_results(self):
        """Search results based on search entry"""
        search_term = self.search_entry.get().lower()
        
        if not search_term:
            # Reset filters and show all results
            self.class_var.set("All Classes")
            self.subject_var.set("All Results")
            self._load_tab_data()
            return
        
        # Get fresh data for searching
        all_results = results_data.get_all() or []
        
        # Sort by creation date first (latest first)
        all_results.sort(key=lambda x: x.get('created_at', 0), reverse=True)
        
        filtered_results = [
            r for r in all_results
            if (search_term in str(r.get('id', '')).lower() or
               search_term in str(r.get('class', '')).lower() or
               search_term in str(r.get('class_incharge', '')).lower() or
               search_term in str(r.get('section', '')).lower())
        ]
        
        print(f"Search found {len(filtered_results)} results for '{search_term}'")
        
        # Store original results
        temp_results = self.results
        self.results = filtered_results
        
        # Update table
        self.populate_table()
        self.count_label.configure(text=f"Search results: {len(filtered_results)}")
        
        # Restore original results (but not display)
        self.results = temp_results
    
    def on_tab_selected(self):
        """Called when this tab is selected"""
        try:
            # Show loading indicator
            self.content.pack_forget()
            self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.progress_bar.start()
            
            # Update status first
            self.status_label.configure(text="Loading results data...", text_color="#FFBE0B")
            
            # Fetch data in a safe way
            self.after(10, self._load_tab_data)
        except Exception as e:
            print(f"Error in on_tab_selected: {e}")
            # Hide loading indicator in case of error
            self.progress_bar.stop()
            self.loading_frame.place_forget()
            self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    def _load_tab_data(self):
        """Load data when tab is selected (safely on main thread)"""
        try:
            # Add a small delay to make loading visible
            def fetch_data():
                try:
                    # Get the data
                    all_results = results_data.get_all()
                    
                    # Make sure we have a valid list
                    if all_results is None:
                        all_results = []
                            
                        # Sort results by created_at timestamp (latest first)
                        all_results.sort(key=lambda x: x.get('created_at', 0), reverse=True)
                        
                    self.results = all_results
                    print(f"Loaded {len(self.results)} results")
                    
                    # Update UI
                    self.populate_table()
                    self.count_label.configure(text=f"Total results: {len(self.results)}")
                    
                    # Update status
                    self.status_label.configure(text="Results data loaded", text_color="#4CC9F0")
                    self.after(3000, lambda: self.status_label.configure(
                        text="📡 Real-time updates enabled",
                        text_color="#4CC9F0"
                    ))
                            
                        # Hide loading indicator and show content
                    self.progress_bar.stop()
                    self.loading_frame.place_forget()
                    self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
                except Exception as e:
                    print(f"Error loading tab data: {e}")
                    self.status_label.configure(text=f"Error loading data: {e}", text_color="#E76F51")
                            
                    # Hide loading indicator in case of error
                    self.progress_bar.stop()
                    self.loading_frame.place_forget()
                    self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
                
                    # Add artificial delay of 1.5 seconds to see the loading animation
                    self.after(1500, fetch_data)
            fetch_data()     
        except Exception as e:
            print(f"Error in _load_tab_data outer function: {e}")
            # Hide loading indicator in case of error
            self.progress_bar.stop()
            self.loading_frame.place_forget()
            self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    def cleanup(self):
        """Clean up resources when component is no longer needed"""
        if hasattr(self, 'unsubscribe'):
            try:
                self.unsubscribe()
                print("Unsubscribed from results updates")
            except Exception as e:
                print(f"Error unsubscribing from updates: {e}")
    
    def add_demo_result(self):
        """Add a demo result entry for testing"""
        # Add a sample result with the exact structure provided
        result_id = result_helpers.add_sample_result_to_database()
        print(f"Added sample result with ID: {result_id}")
        
        # Show notification
        self.status_label.configure(text="✅ Demo result added!", text_color="#4CC9F0")
        
        # Refresh the data after adding
        self.after(100, self._load_tab_data)
        
        # Reset status after 3 seconds
        self.after(3000, lambda: self.status_label.configure(
            text="📊 Results Component Ready",
            text_color="#4CC9F0"
        )) 