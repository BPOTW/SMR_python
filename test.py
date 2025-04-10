import pandas as pd
from fpdf import FPDF
import os

class ResultSheetGenerator:
    def __init__(self, institution_name="SUPERIOR COLLEGE MIAN CHANNU", exam_title="RESULT ( T1 - 2025 )"):
        self.institution_name = institution_name
        self.exam_title = exam_title
        self.students = []
        
    def add_student(self, roll_no, name, biology_math, physics, chemistry_computer, 
                   english, urdu, quran, islamiat_pakstudies):
        """Add a student with their marks to the result sheet."""
        total_obtained = sum([biology_math, physics, chemistry_computer, 
                             english, urdu, quran, islamiat_pakstudies])
        
        # Assuming each subject has 100 marks
        total_marks = 700
        percentage = (total_obtained / total_marks) * 100 if total_marks > 0 else 0
        
        student = {
            'Roll No': roll_no,
            'Student Name': name,
            'Biology/Math': biology_math,
            'Physics': physics,
            'Chemistry/Computer': chemistry_computer,
            'English': english,
            'Urdu': urdu,
            'Quran': quran,
            'Islamiat/Pak-studies': islamiat_pakstudies,
            'Obtained Marks': total_obtained,
            'Total Marks': total_marks,
            'Percentage': round(percentage, 2)
        }
        
        self.students.append(student)
        return student
    
    def generate_excel(self, filename="result_sheet.xlsx"):
        """Generate an Excel file with the result data."""
        if not self.students:
            print("No students added to the result sheet.")
            return
        
        df = pd.DataFrame(self.students)
        df.to_excel(filename, index=False)
        print(f"Excel file generated: {filename}")
    
    def generate_pdf(self, filename="result_sheet.pdf"):
        """Generate a PDF file with the result data formatted like the template."""
        if not self.students:
            print("No students added to the result sheet.")
            return
            
        # Create PDF object with landscape orientation to fit all columns
        pdf = FPDF(orientation='P')
        pdf.add_page()
        
        # Set margins to fit more content
        pdf.set_left_margin(5)
        pdf.set_right_margin(5)
        
        # Set font for title
        pdf.set_font("Arial", "B", 10)
        
        # Title
        pdf.cell(0, 10, self.institution_name, 0, 1, "C")
        pdf.cell(0, 10, self.exam_title, 0, 1, "C")
        
        # Add space
        pdf.ln(2)
        
        # Define column widths that fit within the page width
        # Total available width in landscape mode is around 277mm
        column_widths = [10, 33, 15, 15, 15, 15, 15, 15, 16, 16, 16, 15]
        headers = ["Roll No", "Student Name", "Biology", "Physics", "Chemistry", 
                   "English", "Urdu", "Quran", "Pak-studies", "Obtained Marks", "Total Marks", "Percentage"]
        
        # Set cell height
        cell_height = 6
        
        # Draw header row with black background and white text
        pdf.set_font("Arial", "B", 6)
        pdf.set_fill_color(0, 0, 0)  # Black background
        pdf.set_text_color(255, 255, 255)  # White text
        
        for i, header in enumerate(headers):
            pdf.cell(column_widths[i], cell_height, header, 1, 0, "C", True)
        pdf.ln(cell_height)
        
        # Reset text color for content
        pdf.set_text_color(0, 0, 0)  # Black text
        pdf.set_font("Arial", "", 6)
        
        # Table content
        for student in self.students:
            values = list(student.values())
            
            # Format percentage with % symbol
            values[-1] = f"{values[-1]}%"
            
            for i, value in enumerate(values):
                pdf.cell(column_widths[i], cell_height, str(value), 1, 0, "C")
            pdf.ln(cell_height)
        
        # Output the PDF
        pdf.output(filename)
        print(f"PDF file generated: {filename}")

# Example usage
# if __name__ == "__main__":
#     # Create a result sheet generator
#     generator = ResultSheetGenerator()
    
#     # Add some sample students with their marks
#     generator.add_student(1, "Zain Ali", 85, 78, 82, 90, 88, 95, 92)
#     generator.add_student(2, "Asad Khan", 92, 88, 75, 85, 79, 90, 88)
#     generator.add_student(3, "Fatima Ahmed", 95, 90, 92, 88, 85, 96, 90)
#     generator.add_student(4, "Ayesha Malik", 88, 82, 79, 90, 87, 92, 85)
#     generator.add_student(5, "Hassan Ali", 76, 82, 78, 85, 80, 88, 90)
    
#     # Generate Excel and PDF files
#     generator.generate_excel()
#     generator.generate_pdf()