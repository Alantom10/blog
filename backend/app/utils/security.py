import html
import re
from typing import Any, Dict

def sanitize_string(value: str) -> str:
    """Sanitize string input to prevent XSS"""
    if not isinstance(value, str):
        return value
    
    # HTML encode to prevent XSS
    value = html.escape(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Limit length to prevent DoS
    return value[:10000]

def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively sanitize dictionary values, skipping blog content"""
    sanitized = {}
    for key, value in data.items():
        if key == "content":  
            # Allow HTML content (already from trusted source like Quill)
            sanitized[key] = value
        elif isinstance(value, str):
            sanitized[key] = sanitize_string(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_string(v) if isinstance(v, str) else v for v in value]
        else:
            sanitized[key] = value
    return sanitized
