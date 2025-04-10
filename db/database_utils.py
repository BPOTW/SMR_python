from db.firebase_config import FirebaseConfig
from typing import List, Dict, Any, Optional, Union, Callable
import datetime

class DatabaseUtils:
    """
    Utility class for common database operations
    """
    
    @staticmethod
    def get_collection_data(collection_name: str, limit: int = 100000) -> List[Dict[str, Any]]:
        """
        Get data from a collection with optional limit
        
        Args:
            collection_name (str): Name of the collection to fetch data from
            limit (int): Maximum number of documents to fetch
            
        Returns:
            List[Dict[str, Any]]: List of documents as dictionaries
        """
        try:
            db = FirebaseConfig.get_db()
            collection = db.collection(collection_name)
            
            # Get the documents
            docs = collection.stream()
            
            # Convert to list of dictionaries with document IDs
            # print(docs)
            result = []
            count = 0
            
            for doc in docs:
                if count >= limit:
                    break
                    
                data = doc.to_dict()
                data['id'] = doc.id
                
                # Convert timestamp fields to readable strings
                for key, value in data.items():
                    if isinstance(value, datetime.datetime):
                        data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                
                result.append(data)
                count += 1
            
            return result
        except Exception as e:
            print(f"Error getting data from collection {collection_name}: {e}")
            return []
    
    @staticmethod
    def get_document_by_id(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single document by its ID
        
        Args:
            collection_name (str): Name of the collection
            document_id (str): ID of the document to fetch
            
        Returns:
            Optional[Dict[str, Any]]: Document data as dictionary or None if not found
        """
        try:
            db = FirebaseConfig.get_db()
            doc_ref = db.collection(collection_name).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                
                # Convert timestamp fields to readable strings
                for key, value in data.items():
                    if isinstance(value, datetime.datetime):
                        data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                        
                return data
            else:
                print(f"Document {document_id} not found in collection {collection_name}")
                return None
        except Exception as e:
            print(f"Error getting document {document_id}: {e}")
            return None
    
    @staticmethod
    def query_collection(
        collection_name: str, 
        field: str,
        operator: str,
        value: Any,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query a collection with a simple filter
        
        Args:
            collection_name (str): Name of the collection to query
            field (str): Field to filter on
            operator (str): Comparison operator ('==', '>', '<', '>=', '<=', '!=')
            value (Any): Value to compare against
            limit (int): Maximum number of documents to fetch
            
        Returns:
            List[Dict[str, Any]]: List of documents matching the query
        """
        try:
            db = FirebaseConfig.get_db()
            collection = db.collection(collection_name)
            
            # Create the query
            query = collection.where(field, operator, value)
            
            # Execute the query
            docs = query.stream()
            
            # Convert to list of dictionaries with document IDs
            result = []
            count = 0
            
            for doc in docs:
                if count >= limit:
                    break
                    
                data = doc.to_dict()
                data['id'] = doc.id
                
                # Convert timestamp fields to readable strings
                for key, value in data.items():
                    if isinstance(value, datetime.datetime):
                        data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                
                result.append(data)
                count += 1
            
            return result
        except Exception as e:
            print(f"Error querying collection {collection_name}: {e}")
            return []
    
    @staticmethod
    def add_document(collection_name: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Add a new document to a collection
        
        Args:
            collection_name (str): Name of the collection
            data (Dict[str, Any]): Document data to add
            
        Returns:
            Optional[str]: New document ID if successful, None otherwise
        """
        try:
            db = FirebaseConfig.get_db()
            collection = db.collection(collection_name)
            
            # Add timestamps
            data['created_at'] = datetime.datetime.now()
            data['updated_at'] = datetime.datetime.now()
            
            # Add the document
            _, doc_ref = collection.add(data)
            return doc_ref.id
        except Exception as e:
            print(f"Error adding document to {collection_name}: {e}")
            return None
    
    @staticmethod
    def update_document(collection_name: str, document_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing document
        
        Args:
            collection_name (str): Name of the collection
            document_id (str): ID of the document to update
            data (Dict[str, Any]): New data to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            db = FirebaseConfig.get_db()
            doc_ref = db.collection(collection_name).document(document_id)
            
            # Add update timestamp
            data['updated_at'] = datetime.datetime.now()
            
            # Update the document
            doc_ref.update(data)
            return True
        except Exception as e:
            print(f"Error updating document {document_id}: {e}")
            return False
    
    @staticmethod
    def delete_document(collection_name: str, document_id: str) -> bool:
        """
        Delete a document
        
        Args:
            collection_name (str): Name of the collection
            document_id (str): ID of the document to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            db = FirebaseConfig.get_db()
            doc_ref = db.collection(collection_name).document(document_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"Error deleting document {document_id}: {e}")
            return False
    
    @staticmethod
    def watch_collection(collection_name: str, callback: Callable[[List[Dict[str, Any]]], None]) -> Callable[[], None]:
        """
        Set up a real-time listener for a collection
        
        Args:
            collection_name (str): Name of the collection to watch
            callback (Callable): Function to call when data changes
            
        Returns:
            Callable[[], None]: Function to call to unsubscribe from updates
        """
        try:
            db = FirebaseConfig.get_db()
            collection = db.collection(collection_name)
            
            # Set up the snapshot listener
            def on_snapshot(snapshot, changes, read_time):
                # Convert snapshot to list of dictionaries
                docs = []
                for doc in snapshot:
                    data = doc.to_dict()
                    data['id'] = doc.id
                    
                    # Convert timestamp fields to readable strings
                    for key, value in data.items():
                        if isinstance(value, datetime.datetime):
                            data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                    
                    docs.append(data)
                
                # Call the callback with the updated data
                callback(docs)
            
            # Start listening and return the unsubscribe function
            return collection.on_snapshot(on_snapshot)
        except Exception as e:
            print(f"Error setting up watch on collection {collection_name}: {e}")
            # Return a no-op unsubscribe function
            return lambda: None 


    