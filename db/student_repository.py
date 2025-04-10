from db.data_access import DataAccess
from firebase_admin import firestore
import datetime

class StudentRepository:
    """
    Repository class for student data operations
    """
    
    def __init__(self):
        # Use the DataAccess class to interact with the students collection
        self.data_access = DataAccess('students')
    
    def get_all(self):
        """
        Get all students from the database
        
        Returns:
            list: List of student dictionaries
        """
        return self.data_access.get_all()
    
    def get_by_id(self, student_id):
        """
        Get a student by ID
        
        Args:
            student_id (str): Student ID
            
        Returns:
            dict: Student data or None if not found
        """
        return self.data_access.get_by_id(student_id)
    
    def add(self, student_data):
        """
        Add a new student
        
        Args:
            student_data (dict): Student data
            
        Returns:
            str: ID of the created student or None if failed
        """
        # Timestamps are automatically added by the DataAccess class
        return self.data_access.add(student_data)
    
    def update(self, student_id, student_data):
        """
        Update a student
        
        Args:
            student_id (str): Student ID
            student_data (dict): Student data to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        # Timestamps are automatically updated by the DataAccess class
        return self.data_access.update(student_id, student_data)
    
    def delete(self, student_id):
        """
        Delete a student
        
        Args:
            student_id (str): Student ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        return self.data_access.delete(student_id)
    
    def search(self, query):
        """
        Search for students by name, class, or status
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching student dictionaries
        """
        try:
            # Convert query to lowercase for case-insensitive search
            query = query.lower()
            
            # Get all students - Firestore doesn't natively support full text search
            # so we do this in memory for a simple implementation
            students = self.get_all()
            
            # Filter students based on search query
            results = []
            for student in students:
                # Check if query matches any of these fields
                if (query in student.get('name', '').lower() or
                    query in student.get('class', '').lower() or
                    query in student.get('status', '').lower() or
                    query in student.get('id', '').lower() or
                    query in student.get('phone', '').lower()):
                    results.append(student)
            
            return results
        except Exception as e:
            print(f"Error searching students: {e}")
            return []
    
    def get_by_class(self, class_name):
        """
        Get students by class
        
        Args:
            class_name (str): Class name
            
        Returns:
            list: List of student dictionaries in the specified class
        """
        # Use the query method to filter by class
        return self.data_access.query('class', '==', class_name)
    
    def get_active_students(self):
        """
        Get all active students
        
        Returns:
            list: List of active student dictionaries
        """
        # Use the query method to filter by status
        return self.data_access.query('status', '==', 'Active')
            
    def count_students(self):
        """
        Count the total number of students
        
        Returns:
            int: Number of students
        """
        # Get all students and count them
        return len(self.get_all())
    
    def subscribe_to_changes(self, callback):
        """
        Subscribe to real-time updates of student data
        
        Args:
            callback (function): Callback function to be called when data changes
            
        Returns:
            function: Unsubscribe function to stop listening for changes
        """
        # Use the watch method to subscribe to changes
        return self.data_access.watch(callback) 