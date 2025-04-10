"""
Simple script to test database connections
"""

from db.firebase_config import FirebaseConfig
from db.data_access import students_data, teachers_data, courses_data, results_data
from db.teacher_repository import TeacherRepository
from db.course_repository import CourseRepository

def main():
    print("Initializing Firebase...")
    FirebaseConfig.initialize()
    print("Firebase initialized")
    
    # Test students_data
    print("\nTesting students_data...")
    try:
        students = students_data.get_all()
        print(f"Found {len(students)} students")
        if students:
            print(f"First student: {students[0]}")
    except Exception as e:
        print(f"Error fetching students: {e}")
    
    # Test teachers_data
    print("\nTesting teachers_data...")
    try:
        teachers = teachers_data.get_all()
        print(f"Found {len(teachers)} teachers")
        if teachers:
            print(f"First teacher: {teachers[0]}")
    except Exception as e:
        print(f"Error fetching teachers: {e}")
    
    # Test TeacherRepository
    print("\nTesting TeacherRepository...")
    try:
        teacher_repo = TeacherRepository()
        teachers = teacher_repo.get_all()
        print(f"Found {len(teachers)} teachers via repository")
        if teachers:
            print(f"First teacher: {teachers[0]}")
    except Exception as e:
        print(f"Error with TeacherRepository: {e}")
    
    # Test courses_data
    print("\nTesting courses_data...")
    try:
        courses = courses_data.get_all()
        print(f"Found {len(courses)} courses")
        if courses:
            print(f"First course: {courses[0]}")
    except Exception as e:
        print(f"Error fetching courses: {e}")
    
    # Test CourseRepository
    print("\nTesting CourseRepository...")
    try:
        course_repo = CourseRepository()
        courses = course_repo.get_all()
        print(f"Found {len(courses)} courses via repository")
        if courses:
            print(f"First course: {courses[0]}")
    except Exception as e:
        print(f"Error with CourseRepository: {e}")
    
    # Test results_data
    print("\nTesting results_data...")
    try:
        results = results_data.get_all()
        print(f"Found {len(results)} results")
        if results:
            print(f"First result: {results[0]}")
    except Exception as e:
        print(f"Error fetching results: {e}")

if __name__ == "__main__":
    main() 