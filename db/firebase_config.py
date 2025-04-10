import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json
import uuid
from datetime import datetime

class MockFirestore:
    """
    A mock implementation of Firestore for when Firebase is not available
    """
    def __init__(self):
        self.collections = {}
    
    def collection(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection(name)
        return self.collections[name]

class MockCollection:
    """
    A mock implementation of a Firestore collection
    """
    def __init__(self, name):
        self.name = name
        self.documents = {}
    
    def document(self, doc_id):
        if doc_id not in self.documents:
            self.documents[doc_id] = MockDocument(doc_id, {})
        return self.documents[doc_id]
    
    def add(self, data):
        doc_id = str(uuid.uuid4())
        doc = MockDocument(doc_id, data)
        self.documents[doc_id] = doc
        return None, doc
    
    def stream(self):
        return list(self.documents.values())
    
    def where(self, field, op, value):
        return MockQuery(self, field, op, value)
    
    def on_snapshot(self, callback):
        """Mock on_snapshot that just returns a no-op unsubscribe function"""
        def unsubscribe():
            pass
        return unsubscribe

class MockDocument:
    """
    A mock implementation of a Firestore document
    """
    def __init__(self, id, data):
        self.id = id
        self._data = data
    
    def get(self):
        return self
    
    @property
    def exists(self):
        return True
    
    def to_dict(self):
        return self._data
    
    def set(self, data):
        self._data = data
    
    def update(self, data):
        self._data.update(data)
    
    def delete(self):
        pass

class MockQuery:
    """
    A mock implementation of a Firestore query
    """
    def __init__(self, collection, field, op, value):
        self.collection = collection
        self.field = field
        self.op = op
        self.value = value
    
    def stream(self):
        results = []
        for doc in self.collection.documents.values():
            if self.field in doc._data:
                if self.op == '==' and doc._data[self.field] == self.value:
                    results.append(doc)
        return results

class FirebaseConfig:
    """
    Firebase configuration class for handling the connection to Firebase
    """
    _instance = None
    _db = None
    _use_mock = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
            # Initialize with empty values to be set up later
            cls._cred = None
            cls._app = None
            cls._db = None
            cls._mock_db = MockFirestore()
            cls._use_mock = False
        return cls._instance
    
    @classmethod
    def initialize(cls, credentials_path=None, service_account_info=None):
        """
        Initialize the Firebase Admin SDK with credentials
        
        Args:
            credentials_path (str): Path to service account key file
            service_account_info (dict): Service account info as dictionary
        
        Returns:
            bool: True if initialized successfully, False otherwise
        """
        try:
            if credentials_path and os.path.exists(credentials_path):
                # Initialize using credential file
                cls._cred = credentials.Certificate(credentials_path)
            elif service_account_info:
                # Initialize using service account info
                cls._cred = credentials.Certificate(service_account_info)
            else:
                # If no service account info is provided, try to get from environment variables
                service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
                if service_account_json:
                    service_account_info = json.loads(service_account_json)
                    cls._cred = credentials.Certificate(service_account_info)
                else:
                    # For testing purposes, use mock implementation
                    print("Warning: No credentials provided. Using mock implementation.")
                    cls._use_mock = True
                    return True
                    
            # Initialize the app with credentials if we got them
            if cls._cred:
                try:
                    cls._app = firebase_admin.initialize_app(cls._cred)
                    cls._db = firestore.client()
                    return True
                except Exception as e:
                    print(f"Error initializing Firebase with credentials: {e}")
                    print("Using mock implementation for development.")
                    cls._use_mock = True
                    return True
            else:
                print("Error: Firebase initialization failed. No valid credentials provided.")
                print("Using mock implementation for development.")
                cls._use_mock = True
                return True
            
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            print("Using mock implementation for development.")
            cls._use_mock = True
            return True
    
    @classmethod
    def get_db(cls):
        """
        Get the Firestore database instance
        
        Returns:
            firestore.Client: Firestore client instance
        """
        if cls._db is None and not cls._use_mock:
            # Try to initialize with default settings if not already initialized
            cls.initialize()
        
        if cls._use_mock:
            # Ensure we have a mock instance
            if not hasattr(cls, '_mock_db') or cls._mock_db is None:
                cls._mock_db = MockFirestore()
            return cls._mock_db
        
        return cls._db
    
    @classmethod
    def is_initialized(cls):
        """
        Check if Firebase has been initialized
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return cls._db is not None or cls._use_mock
    
    @classmethod
    def close(cls):
        """
        Close the Firebase connection
        """
        if cls._app:
            try:
                firebase_admin.delete_app(cls._app)
                cls._app = None
                cls._db = None
                cls._cred = None
            except Exception as e:
                print(f"Error closing Firebase connection: {e}") 