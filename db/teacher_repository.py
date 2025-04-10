from db.data_access import DataAccess
from firebase_admin import firestore
import datetime

class TeacherRepository:
    """
    Repository class for teacher data operations
    """
    
    def __init__(self):
        # Use the DataAccess class to interact with the teachers collection
        self.data_access = DataAccess('teachers')
    
    def get_all(self):
        """
        Get all teachers from the database
        
        Returns:
            list: List of teacher dictionaries
        """
        return self.data_access.get_all()
    
    def get_by_id(self, teacher_id):
        """
        Get a teacher by ID
        
        Args:
            teacher_id (str): Teacher ID
            
        Returns:
            dict: Teacher data or None if not found
        """
        return self.data_access.get_by_id(teacher_id)
    
    def add(self, teacher_data):
        """
        Add a new teacher
        
        Args:
            teacher_data (dict): Teacher data
            
        Returns:
            str: ID of the created teacher or None if failed
        """
        # Timestamps are automatically added by the DataAccess class
        return self.data_access.add(teacher_data)
    
    def update(self, teacher_id, teacher_data):
        """
        Update a teacher
        
        Args:
            teacher_id (str): Teacher ID
            teacher_data (dict): Teacher data to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        # Timestamps are automatically updated by the DataAccess class
        return self.data_access.update(teacher_id, teacher_data)
    
    def delete(self, teacher_id):
        """
        Delete a teacher
        
        Args:
            teacher_id (str): Teacher ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        return self.data_access.delete(teacher_id)
    
    def search(self, query):
        """
        Search for teachers by name, subject, or status
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching teacher dictionaries
        """
        try:
            # Convert query to lowercase for case-insensitive search
            query = query.lower()
            
            # Get all teachers - Firestore doesn't natively support full text search
            # so we do this in memory for a simple implementation
            teachers = self.get_all()
            
            # Filter teachers based on search query
            results = []
            for teacher in teachers:
                # Check if query matches any of these fields
                if (query in teacher.get('name', '').lower() or
                    query in teacher.get('subject', '').lower() or
                    query in teacher.get('status', '').lower() or
                    query in teacher.get('id', '').lower() or
                    query in teacher.get('phone', '').lower()):
                    results.append(teacher)
            
            return results
        except Exception as e:
            print(f"Error searching teachers: {e}")
            return []
    
    def get_by_subject(self, subject):
        """
        Get teachers by subject
        
        Args:
            subject (str): Subject name
            
        Returns:
            list: List of teacher dictionaries teaching the specified subject
        """
        # Use the query method to filter by subject
        return self.data_access.query('subject', '==', subject)
    
    def get_active_teachers(self):
        """
        Get all active teachers
        
        Returns:
            list: List of active teacher dictionaries
        """
        # Use the query method to filter by status
        return self.data_access.query('status', '==', 'Active')
            
    def count_teachers(self):
        """
        Count the total number of teachers
        
        Returns:
            int: Number of teachers
        """
        # Get all teachers and count them
        return len(self.get_all())
        
    def subscribe_to_changes(self, callback):
        """
        Subscribe to real-time updates of teacher data
        
        Args:
            callback (function): Callback function to be called when data changes
            
        Returns:
            function: Unsubscribe function to stop listening for changes
        """
        # Use the watch method to subscribe to changes
        return self.data_access.watch(callback) 