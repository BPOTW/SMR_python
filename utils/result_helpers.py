from db.data_access import results_data
import datetime

def create_result_entry(class_number, section, class_incharge, test_name, max_marks, subjects_data):
    """
    Create a structured result entry ready to be added to the database
    
    Args:
        class_number (int): Class/grade number
        section (str): Section name (e.g., 'mb-blue')
        class_incharge (str): Name of class incharge/teacher
        test_name (str): Name of the test
        max_marks (int): Maximum marks for the test
        subjects_data (dict): Dictionary of subjects and their data
    Returns:
        dict: Structured result data
    """
    # Initialize result data structure
    result_data = {
        'class': class_number,
        'class_incharge': class_incharge,
        'completed': False,
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'marks': {},
        'max_marks': {},
        'maxMarks':max_marks,
        'section': section,
        'status': subjects_data,
        'strength': 0,
        'test_name': test_name,
        'updated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
        'uploaded_by': {}
    }

    #return the result data
    id = add_result_to_database(result_data)
    return id

def add_result_to_database(result_data):
    """
    Add a prepared result entry to the Firebase database
    
    Args:
        result_data (dict): The structured result data to add
        
    Returns:
        str: The ID of the newly added document or None if failed
    """
    return results_data.add(result_data)

def create_result_data(class_number, section, class_incharge):
    """
    Create and add a new result entry to the database
    
    Returns:
        str: The ID of the newly added document or None if failed
    """
    # Sample data
    class_number = class_number
    section = section
    class_incharge = class_incharge
    students = []
    created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subjects = ["chemistry", "urdu", "biology", "islamiat", "pak-studies", 
                "physics", "quran", "english"]
    teachers = {
        "chemistry": "",
        "urdu": "",
        "biology": "",
        "islamiat": "",
        "pak-studies": "",
        "physics": "",
        "quran": "",
        "english": ""
    }
    
    # Create the result structure
    result_data = create_result_entry(
        class_number, 
        section, 
        class_incharge, 
        students, 
        subjects, 
        teachers
    )
    
    # # Set some scores and statuses (to match your example)
    # result_data["urdu"]["ali"] = 1
    # result_data["urdu"]["zain"] = 1
    # result_data["islamiat"]["ali"] = 1
    # result_data["islamiat"]["zain"] = 1
    # result_data["physics"]["ali"] = 1
    # result_data["physics"]["zain"] = 1
    # result_data["quran"]["ali"] = 1
    # result_data["quran"]["zain"] = 1
    
    # Update statuses
    for subject in subjects:
        subject_key = subject.lower().replace(' ', '-')
        result_data["status"][subject_key] = "Pending"
    
    
    # Add to database
    return add_result_to_database(result_data)

def add_sample_result_to_database():
    """
    Add a sample result directly to the database with the exact structure shown in the example
    
    Returns:
        str: The document ID if successful, None otherwise
    """
    # Create the exact structure from the example
    result_data = {
        'class': 11,
        'section': 'mb-blue',
        'class_incharge': 'Ahsan Anam Javeed', 
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'chemistry': {
            'ali': 85, 
            'zain': 78
        }, 
        'urdu': {
            'ali': 92, 
            'zain': 88
        }, 
        'biology': {
            'ali': 76, 
            'zain': 82
        }, 
        'islamiat': {
            'ali': 95, 
            'zain': 90
        }, 
        'pak-studies': {
            'ali': 88, 
            'zain': 85
        }, 
        'quran': {
            'ali': 98, 
            'zain': 96
        }, 
        'physics': {
            'ali': 82, 
            'zain': 79
        }, 
        'english': {
            'ali': 89, 
            'zain': 84
        },
        'uploaded_by': {
            'urdu': 'yTeacher', 
            'islamiat': 'cTeacher', 
            'english': 'xTeacher', 
            'biology': 'zTeacher', 
            'pak-studies': 'dTeacher', 
            'physics': 'aTeacher', 
            'chemistry': 'bTeacher', 
            'quran': 'eTeacher'
        },
        'status': {
            'urdu': 'ready', 
            'islamiat': 'ready', 
            'biology': 'ready', 
            'pak-studies': 'ready', 
            'physics': 'ready', 
            'quran': 'ready', 
            'chemistry': 'Ready', 
            'english': 'ready'
        }
    }
    
    # Add to database
    return results_data.add(result_data)



    # {
    #     'class': 11,
    #     'section': 'mb-blue', 
    #     'id': '93UIkiCwtcj8La4UPZBd', 
    #     'class_incharge': 'Ahsan Anam Javeed', 
    #     'created_at': '2025-03-28 21:38:31', 
    #     'chemistry': {
    #         'ali': 0, 
    #         'zain': 0
    #     }, 
    #     'urdu': {
    #         'ali': 1, 
    #         'zain': 1
    #     }, 
    #     'biology': {
    #         'ali': 0, 
    #         'zain': 0
    #     }, 
    #     'islamiat': {
    #         'ali': 1, 
    #         'zain': 1
    #     }, 
    #     'pak-studies': {
    #         'ali': 0, 
    #         'zain': 0
    #     }, 
    #     'quran': {
    #         'ali': 1, 
    #         'zain': 1
    #     }, 
    #     'physics': {
    #         'ali': 1, 
    #         'zain': 1
    #     }, 
    #     'english': {
    #         'ali': 0, 
    #         'zain': 0
    #     },
    #     'uploaded_by': {
    #         'urdu': 'yTeacher', 
    #         'islamiat': 'cTeacher', 
    #         'english': 'xTeaxher', 
    #         'biology': 'zTeacher', 
    #         'pak-studies': 'dTeacher', 
    #         'physics': 'aTeacher', 
    #         'chemistry': 'bTeacher', 
    #         'quran': 'eTeacher', 
    #     },
    #     'status': {
    #         'urdu': 'ready', 
    #         'islamiat': 'ready', 
    #         'biology': 'ready', 
    #         'pak-studies': 'ready', 
    #         'physics': 'ready', 
    #         'quran': 'ready', 
    #         'chemistry': 'Ready', 
    #         'english': 'ready'
    #         }, 
    # }        