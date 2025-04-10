from db.data_access import DataAccess
from firebase_admin import firestore
import datetime

class CourseRepository:
    """
    Repository class for course data operations
    """
    
    def __init__(self):
        # Use the DataAccess class to interact with the courses collection
        self.data_access = DataAccess('courses')
    
    def get_all(self):
        """
        Get all courses from the database
        
        Returns:
            list: List of course dictionaries
        """
        return self.data_access.get_all()
    
    def get_by_id(self, course_id):
        """
        Get a course by ID
        
        Args:
            course_id (str): Course ID
            
        Returns:
            dict: Course data or None if not found
        """
        return self.data_access.get_by_id(course_id)
    
    def add(self, course_data):
        """
        Add a new course
        
        Args:
            course_data (dict): Course data
            
        Returns:
            str: ID of the created course or None if failed
        """
        # Timestamps are automatically added by the DataAccess class
        return self.data_access.add(course_data)
    
    def update(self, course_id, course_data):
        """
        Update a course
        
        Args:
            course_id (str): Course ID
            course_data (dict): Course data to update
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        # Timestamps are automatically updated by the DataAccess class
        return self.data_access.update(course_id, course_data)
    
    def delete(self, course_id):
        """
        Delete a course
        
        Args:
            course_id (str): Course ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        return self.data_access.delete(course_id)
    
    def search(self, query):
        """
        Search for courses by name, teacher, or status
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching course dictionaries
        """
        try:
            # Convert query to lowercase for case-insensitive search
            query = query.lower()
            
            # Get all courses - Firestore doesn't natively support full text search
            # so we do this in memory for a simple implementation
            courses = self.get_all()
            
            # Filter courses based on search query
            results = []
            for course in courses:
                # Check if query matches any of these fields
                if (query in course.get('name', '').lower() or
                    query in course.get('teacher', '').lower() or
                    query in course.get('status', '').lower() or
                    query in course.get('id', '').lower() or
                    query in str(course.get('students', '')).lower()):
                    results.append(course)
            
            return results
        except Exception as e:
            print(f"Error searching courses: {e}")
            return []
    
    def get_by_teacher(self, teacher_name):
        """
        Get courses by teacher
        
        Args:
            teacher_name (str): Teacher name
            
        Returns:
            list: List of course dictionaries taught by the specified teacher
        """
        # Use the query method to filter by teacher
        return self.data_access.query('teacher', '==', teacher_name)
    
    def get_active_courses(self):
        """
        Get all active courses
        
        Returns:
            list: List of active course dictionaries
        """
        # Use the query method to filter by status
        return self.data_access.query('status', '==', 'Active')
            
    def count_courses(self):
        """
        Count the total number of courses
        
        Returns:
            int: Number of courses
        """
        # Get all courses and count them
        return len(self.get_all())
    
    def count_students_in_courses(self):
        """
        Count the total number of students enrolled in all courses
        
        Returns:
            int: Total number of students enrolled
        """
        try:
            courses = self.get_all()
            total_students = sum(len(course.get('students', [])) for course in courses)
            return total_students
        except Exception as e:
            print(f"Error counting students in courses: {e}")
            return 0
            
    def subscribe_to_changes(self, callback):
        """
        Subscribe to real-time updates of course data
        
        Args:
            callback (function): Callback function to be called when data changes
            
        Returns:
            function: Unsubscribe function to stop listening for changes
        """
        # Use the watch method to subscribe to changes
        return self.data_access.watch(callback) 