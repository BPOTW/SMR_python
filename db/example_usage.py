from db.database_utils import DatabaseUtils
import time

def main():
    """
    Example usage of database utilities
    """
    print("Database Utilities Example")
    print("=========================")
    
    # Create a collection name for examples
    collection_name = "examples"
    
    # Example 1: Adding a document
    print("\n1. Adding a document...")
    example_data = {
        "name": "Example Item",
        "description": "This is an example item created through the database utilities",
        "status": "active",
        "priority": 1,
        "tags": ["example", "test", "demo"]
    }
    
    doc_id = DatabaseUtils.add_document(collection_name, example_data)
    if doc_id:
        print(f"Document added successfully with ID: {doc_id}")
    else:
        print("Failed to add document")
    
    # Example 2: Getting a document by ID
    print("\n2. Getting a document by ID...")
    if doc_id:
        document = DatabaseUtils.get_document_by_id(collection_name, doc_id)
        if document:
            print(f"Retrieved document: {document}")
        else:
            print("Document not found")
    
    # Example 3: Updating a document
    print("\n3. Updating a document...")
    if doc_id:
        update_data = {
            "description": "This document has been updated",
            "priority": 2,
            "tags": ["example", "test", "updated"]
        }
        
        success = DatabaseUtils.update_document(collection_name, doc_id, update_data)
        if success:
            print("Document updated successfully")
        else:
            print("Failed to update document")
        
        # Get the updated document
        updated_doc = DatabaseUtils.get_document_by_id(collection_name, doc_id)
        if updated_doc:
            print(f"Updated document: {updated_doc}")
    
    # Example 4: Querying documents
    print("\n4. Querying documents...")
    query_results = DatabaseUtils.query_collection(collection_name, "status", "==", "active")
    print(f"Found {len(query_results)} active documents")
    for i, doc in enumerate(query_results):
        print(f"Document {i+1}: {doc}")
    
    # Example 5: Getting all documents in a collection
    print("\n5. Getting all documents in a collection...")
    all_docs = DatabaseUtils.get_collection_data(collection_name)
    print(f"Found {len(all_docs)} documents in collection")
    for i, doc in enumerate(all_docs):
        print(f"Document {i+1}: {doc}")
    
    # Example 6: Real-time updates (watch for changes)
    print("\n6. Watching for changes (will run for 30 seconds)...")
    
    def handle_update(docs):
        print(f"\nCollection updated! Now contains {len(docs)} documents")
        for i, doc in enumerate(docs):
            print(f"Document {i+1}: {doc}")
    
    # Start watching the collection
    unsubscribe = DatabaseUtils.watch_collection(collection_name, handle_update)
    
    # Wait for a while to see if any changes happen
    print("Watching for changes for 30 seconds...")
    print("(Try making changes in another script or in the Firebase console)")
    
    # Wait for 30 seconds
    time.sleep(30)
    
    # Stop watching
    unsubscribe()
    print("Stopped watching for changes")
    
    # Example 7: Deleting a document
    print("\n7. Deleting a document...")
    if doc_id:
        success = DatabaseUtils.delete_document(collection_name, doc_id)
        if success:
            print(f"Document {doc_id} deleted successfully")
        else:
            print(f"Failed to delete document {doc_id}")
    
    print("\nDatabase example complete!")

if __name__ == "__main__":
    main() 