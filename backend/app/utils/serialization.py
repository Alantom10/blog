from typing import Any, Dict
from pydantic import BaseModel, HttpUrl


def serialize_for_mongo(model: BaseModel) -> Dict[str, Any]:
    """
    Converts a Pydantic model into a dict that can be safely inserted into MongoDB.
    
    This utility function handles the conversion of Pydantic models to MongoDB-compatible
    dictionaries by recursively converting problematic types that MongoDB can't serialize.
    
    Key conversions:
    - HttpUrl objects -> string representation
    - Nested objects -> recursively processed dictionaries
    - Lists -> recursively processed lists
    
    Args:
        model: Pydantic BaseModel instance to convert
        
    Returns:
        Dict[str, Any]: MongoDB-compatible dictionary representation
        
    Example:
        blog = Blog(title="Test", slug="test", ...)
        blog_dict = serialize_for_mongo(blog)
        # Ready for MongoDB insertion
    """
    # Convert Pydantic model to dictionary using model_dump()
    data = model.model_dump()

    def convert(obj):
        """
        Recursive helper function to convert objects to MongoDB-compatible types
        
        Args:
            obj: Object to convert (can be any type)
            
        Returns:
            MongoDB-compatible representation of the object
        """
        if isinstance(obj, HttpUrl):
            # Convert Pydantic HttpUrl to string for MongoDB storage
            return str(obj)
        elif isinstance(obj, dict):
            # Recursively convert dictionary values
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Recursively convert list items
            return [convert(i) for i in obj]
        else:
            # Return primitive types as-is (int, str, bool, datetime, etc.)
            return obj

    # Apply recursive conversion to the entire model data
    return convert(data)