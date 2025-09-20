from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with user-friendly messages"""
    errors = []
    for error in exc.errors():
        field = error.get('loc', ['unknown'])[-1]  # Get the field name
        message = error.get('msg', 'Invalid value')
        
        # Convert technical messages to user-friendly ones
        if 'field required' in message.lower():
            message = f"{field} is required"
        elif 'ensure this value has at least' in message.lower():
            message = f"{field} is too short"
        elif 'ensure this value has at most' in message.lower():
            message = f"{field} is too long"
        elif 'value is not a valid email address' in message.lower():
            message = "Please enter a valid email address"
            
        errors.append(f"{field}: {message}")
    
    # Log the validation error for debugging
    logger.warning(f"Validation error on {request.url}: {errors}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation failed",
            "errors": errors
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent formatting"""
    # Log the error for monitoring
    logger.warning(f"HTTP {exc.status_code} on {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors without leaking sensitive info"""
    # Log the full error for debugging
    logger.error(f"Unexpected error on {request.url}: {str(exc)}")
    logger.error(traceback.format_exc())
    
    # Return generic error message to user
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "status_code": 500
        }
    )