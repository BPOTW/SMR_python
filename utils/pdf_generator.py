# Located in utils/pdf_generator.py

import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

class ResultSheetGenerator:
    # Removed max_marks_per_subject, added max_marks_map parameter
    def __init__(self, institution_name="SUPERIOR COLLEGE MIAN CHANNU", exam_title="RESULT", max_marks_map=None):
        self.institution_name = institution_name
        self.exam_title = exam_title
        # Store the map of subject -> max marks. Initialize if None.
        self.max_marks_map = max_marks_map if max_marks_map is not None else {}
        self.students = []
        self.subjects = [] # Subjects will be set externally via set_subjects

    # New method to explicitly set the map if needed after init
    def set_max_marks_map(self, max_marks_map):
        self.max_marks_map = max_marks_map if max_marks_map is not None else {}

    def add_student(self, roll_no, name, *subject_marks):
        if not self.subjects:
            raise ValueError("Subjects must be set using set_subjects() before adding students.")
        if not self.max_marks_map:
             print("Warning: Max marks map is not set. Total marks calculation might be incorrect.")
             # Optionally raise ValueError("Max marks map must be set before adding students.")

        if len(subject_marks) != len(self.subjects):
             raise ValueError(f"Number of marks provided ({len(subject_marks)}) does not match the number of subjects ({len(self.subjects)}).")

        numeric_marks = []
        for mark in subject_marks:
            try:
                numeric_mark = float(mark)
                if numeric_mark.is_integer():
                    numeric_mark = int(numeric_mark)
                numeric_marks.append(numeric_mark)
            except (ValueError, TypeError):
                numeric_marks.append(0)

        total_obtained = sum(numeric_marks)

        # Calculate Total Marks - Sum of all subject max marks
        total_marks = 0
        for subject in self.subjects:
            # Get max marks for the current subject from the map
            try:
                subject_max = int(self.max_marks_map.get(subject, 0))
                total_marks += subject_max
            except (ValueError, TypeError):
                print(f"Warning: Invalid max marks value for subject '{subject}'. Assuming 0.")

        percentage = (total_obtained / total_marks) * 100 if total_marks > 0 else 0

        student = {
            'Roll No': roll_no,
            'Student Name': name
        }
        for i, mark in enumerate(numeric_marks):
            student[self.subjects[i]] = mark

        student['Obtained Marks'] = total_obtained
        student['Total Marks'] = total_marks # Use the dynamically calculated total
        student['Percentage'] = round(percentage, 2)

        self.students.append(student)
        return student

    def set_subjects(self, subject_list):
        self.subjects = subject_list

    def generate_excel(self, filepath="result_sheet.xlsx"):
        # (This method remains unchanged)
        if not self.students:
            print("No students added to the result sheet.")
            return None
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        column_order = ['Roll No', 'Student Name'] + self.subjects + ['Obtained Marks', 'Total Marks', 'Percentage']
        df = pd.DataFrame(self.students)
        df = df[column_order] # Reorder columns
        df.to_excel(filepath, index=False)
        abs_path = os.path.abspath(filepath)
        print(f"Excel file generated: {abs_path}")
        return abs_path

    def generate_pdf(self, filepath=f"result_sheets/{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.pdf"):
         # (This method remains largely unchanged, column widths are still dynamic)
        if not self.students:
            print("No students added to the result sheet.")
            return None
        if not self.subjects:
             print("No subjects set for the result sheet.")
             return None

        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

        pdf = FPDF(orientation='P')
        pdf.add_page()
        pdf.set_left_margin(5)
        pdf.set_right_margin(5)
        page_width = pdf.w - pdf.l_margin - pdf.r_margin

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, self.institution_name, 0, 1, "C")
        pdf.cell(0, 10, self.exam_title, 0, 1, "C")
        pdf.ln(5)

        fixed_widths_config = {
            'Roll No': 12, 'Name': 40, 'Obtained': 18,
            'Total': 18, 'Percentage': 18
        }
        total_fixed_width = sum(fixed_widths_config.values())
        remaining_width = page_width - total_fixed_width
        subject_width = remaining_width / len(self.subjects) if self.subjects else 0

        if subject_width < 10 and len(self.subjects) > 0:
             print(f"Warning: Calculated subject column width ({subject_width:.2f}) is very small.")

        headers = ['Roll No', 'Name'] + self.subjects + ['Obtained', 'Total', 'Percentage']
        column_widths = [
             fixed_widths_config['Roll No'], fixed_widths_config['Name']
             ] + [subject_width] * len(self.subjects) + [
             fixed_widths_config['Obtained'], fixed_widths_config['Total'],
             fixed_widths_config['Percentage']
             ]

        cell_height = 7
        pdf.set_font("Arial", "B", 8)
        pdf.set_fill_color(0, 0, 0)
        pdf.set_text_color(255, 255, 255)

        for i, header in enumerate(headers):
            display_header = (header[:10] + '..') if len(header) > 12 and column_widths[i] < 20 else header
            pdf.cell(column_widths[i], cell_height, str(display_header), 1, 0, "C", True)
        pdf.ln(cell_height)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 8)

        for student in self.students:
            pdf.cell(column_widths[0], cell_height, str(student.get('Roll No', '')), 1, 0, "C")
            pdf.cell(column_widths[1], cell_height, str(student.get('Student Name', '')), 1, 0, "L")

            subject_start_index = 2
            for i, subject in enumerate(self.subjects):
                value = student.get(subject, '')
                pdf.cell(column_widths[subject_start_index + i], cell_height, str(value), 1, 0, "C")

            obtained_index = subject_start_index + len(self.subjects)
            total_index = obtained_index + 1
            percentage_index = total_index + 1

            pdf.cell(column_widths[obtained_index], cell_height, str(student.get('Obtained Marks', '')), 1, 0, "C")
            pdf.cell(column_widths[total_index], cell_height, str(student.get('Total Marks', '')), 1, 0, "C") # Display calculated total
            pdf.cell(column_widths[percentage_index], cell_height, f"{student.get('Percentage', 0):.2f}%", 1, 0, "C")

            pdf.ln(cell_height)

        try:
             pdf.output(filepath)
             abs_path = os.path.abspath(filepath)
             print(f"PDF file generated: {abs_path}")
             return abs_path
        except Exception as e:
             print(f"Error generating PDF: {e}")
             return None