from db.database_utils import DatabaseUtils
from typing import List, Dict, Any, Optional, Callable
import datetime

class DataAccess:
    """
    Data access class for a specific collection
    """
    
    def __init__(self, collection_name: str):
        """
        Initialize the data access for a specific collection
        
        Args:
            collection_name (str): Name of the collection to access
        """
        self.collection_name = collection_name
    
    def get_all(self, limit: int = 100000) -> List[Dict[str, Any]]:
        """
        Get all documents from the collection
        
        Args:
            limit (int): Maximum number of documents to fetch
            
        Returns:
            List[Dict[str, Any]]: List of documents
        """
        # print(self.collection_name)
        return DatabaseUtils.get_collection_data(self.collection_name, limit)
    
    def get_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Optional[Dict[str, Any]]: Document or None if not found
        """
        return DatabaseUtils.get_document_by_id(self.collection_name, doc_id)
    
    def query(self, field: str, operator: str, value: Any, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query the collection
        
        Args:
            field (str): Field to filter on
            operator (str): Comparison operator ('==', '>', '<', '>=', '<=', '!=')
            value (Any): Value to compare against
            limit (int): Maximum number of documents to fetch
            
        Returns:
            List[Dict[str, Any]]: List of matching documents
        """
        return DatabaseUtils.query_collection(
            self.collection_name, 
            field,
            operator,
            value,
            limit
        )
    
    def add(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Add a new document
        
        Args:
            data (Dict[str, Any]): Document data
            
        Returns:
            Optional[str]: New document ID or None if failed
        """
        return DatabaseUtils.add_document(self.collection_name, data)
    
    def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a document
        
        Args:
            doc_id (str): Document ID
            data (Dict[str, Any]): Updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        return DatabaseUtils.update_document(self.collection_name, doc_id, data)
    
    def delete(self, doc_id: str) -> bool:
        """
        Delete a document
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        return DatabaseUtils.delete_document(self.collection_name, doc_id)
    
    def watch(self, callback: Callable[[List[Dict[str, Any]]], None]) -> Callable[[], None]:
        """
        Watch for changes in the collection
        
        Args:
            callback (Callable): Function to call with updated data
            
        Returns:
            Callable[[], None]: Function to call to stop watching
        """
        return DatabaseUtils.watch_collection(self.collection_name, callback)

# Create some common data access objects
students_data = DataAccess("students")
teachers_data = DataAccess("teachers")
courses_data = DataAccess("courses")
results_data = DataAccess("result_data") 