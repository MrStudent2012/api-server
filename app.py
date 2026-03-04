"""
Simple REST API Server with In-Memory Data Store
Mini Project 2: Demonstrates REST API design, CRUD operations, and best practices
"""

from flask import Flask, request, jsonify
from datetime import datetime
import logging
from typing import Dict, Optional, Tuple, Any
import uuid

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# In-memory data store for users
users_db: Dict[str, Dict[str, Any]] = {}


# ==================== VALIDATION FUNCTIONS ====================

def validate_user_data(data: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate user data for POST and PUT requests.
    
    Args:
        data: Dictionary containing user data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Request body cannot be empty"
    
    # Check required fields
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        return False, "Field 'name' is required and must be a non-empty string"
    
    if 'email' not in data or not isinstance(data['email'], str) or not data['email'].strip():
        return False, "Field 'email' is required and must be a non-empty string"
    
    # Validate email format (basic check)
    if '@' not in data['email'] or '.' not in data['email']:
        return False, "Field 'email' must be a valid email address"
    
    # Optional age validation if provided
    if 'age' in data:
        if not isinstance(data['age'], int) or data['age'] < 0 or data['age'] > 150:
            return False, "Field 'age' must be a positive integer between 0 and 150"
    
    return True, None


# ==================== ERROR HANDLING MIDDLEWARE ====================

class APIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


@app.errorhandler(APIError)
def handle_api_error(error: APIError):
    """Handle custom API errors"""
    logger.warning(f"API Error: {error.message} (Status: {error.status_code})")
    return jsonify({
        'success': False,
        'error': error.message,
        'timestamp': datetime.utcnow().isoformat()
    }), error.status_code


@app.errorhandler(400)
def handle_bad_request(error):
    """Handle bad request errors"""
    logger.warning(f"Bad request: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Invalid request format',
        'timestamp': datetime.utcnow().isoformat()
    }), 400


@app.errorhandler(404)
def handle_not_found(error):
    """Handle not found errors"""
    logger.warning(f"Resource not found: {request.path}")
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404


@app.errorhandler(500)
def handle_internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.utcnow().isoformat()
    }), 500


# ==================== REQUEST LOGGING MIDDLEWARE ====================

@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"Incoming request: {request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.info(f"Response: {response.status_code} - {request.method} {request.path}")
    return response


# ==================== CRUD ENDPOINTS ====================

@app.get('/users')
def get_users():
    """
    Get all users
    
    Returns:
        JSON list of all users with 200 status code
    """
    try:
        users_list = list(users_db.values())
        logger.info(f"Retrieved {len(users_list)} users")
        return jsonify({
            'success': True,
            'data': users_list,
            'count': len(users_list),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise APIError("Failed to retrieve users", 500)


@app.get('/users/<user_id>')
def get_user(user_id: str):
    """
    Get a specific user by ID
    
    Args:
        user_id: The user ID
        
    Returns:
        JSON user object with 200 status code or 404 if not found
    """
    if user_id not in users_db:
        logger.warning(f"User not found: {user_id}")
        raise APIError(f"User with ID '{user_id}' not found", 404)
    
    logger.info(f"Retrieved user: {user_id}")
    return jsonify({
        'success': True,
        'data': users_db[user_id],
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.post('/users')
def create_user():
    """
    Create a new user
    
    Request body:
        {
            "name": "string (required)",
            "email": "string (required)",
            "age": "integer (optional)"
        }
    
    Returns:
        JSON user object with 201 status code or 400 if validation fails
    """
    try:
        data = request.get_json()
    except Exception:
        logger.error("Invalid JSON in request body")
        raise APIError("Invalid JSON in request body", 400)
    
    # Validate user data
    is_valid, error_msg = validate_user_data(data)
    if not is_valid:
        logger.warning(f"Validation error: {error_msg}")
        raise APIError(error_msg, 400)
    
    # Create new user
    user_id = str(uuid.uuid4())
    new_user = {
        'id': user_id,
        'name': data['name'].strip(),
        'email': data['email'].strip(),
        'age': data.get('age'),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    users_db[user_id] = new_user
    logger.info(f"User created with ID: {user_id}")
    
    return jsonify({
        'success': True,
        'data': new_user,
        'message': 'User created successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201


@app.put('/users/<user_id>')
def update_user(user_id: str):
    """
    Update an existing user
    
    Args:
        user_id: The user ID to update
        
    Request body:
        {
            "name": "string (optional)",
            "email": "string (optional)",
            "age": "integer (optional)"
        }
    
    Returns:
        JSON updated user object with 200 status code or 404 if not found
    """
    if user_id not in users_db:
        logger.warning(f"User not found for update: {user_id}")
        raise APIError(f"User with ID '{user_id}' not found", 404)
    
    try:
        data = request.get_json()
    except Exception:
        logger.error("Invalid JSON in request body")
        raise APIError("Invalid JSON in request body", 400)
    
    if not data:
        logger.warning("Empty request body for update")
        raise APIError("Request body cannot be empty", 400)
    
    # Validate and update fields
    user = users_db[user_id]
    
    if 'name' in data:
        if not isinstance(data['name'], str) or not data['name'].strip():
            raise APIError("Field 'name' must be a non-empty string", 400)
        user['name'] = data['name'].strip()
    
    if 'email' in data:
        if not isinstance(data['email'], str) or not data['email'].strip():
            raise APIError("Field 'email' must be a non-empty string", 400)
        if '@' not in data['email'] or '.' not in data['email']:
            raise APIError("Field 'email' must be a valid email address", 400)
        user['email'] = data['email'].strip()
    
    if 'age' in data:
        if not isinstance(data['age'], int) or data['age'] < 0 or data['age'] > 150:
            raise APIError("Field 'age' must be a positive integer between 0 and 150", 400)
        user['age'] = data['age']
    
    user['updated_at'] = datetime.utcnow().isoformat()
    logger.info(f"User updated: {user_id}")
    
    return jsonify({
        'success': True,
        'data': user,
        'message': 'User updated successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.delete('/users/<user_id>')
def delete_user(user_id: str):
    """
    Delete a user
    
    Args:
        user_id: The user ID to delete
        
    Returns:
        JSON confirmation with 200 status code or 404 if not found
    """
    if user_id not in users_db:
        logger.warning(f"User not found for deletion: {user_id}")
        raise APIError(f"User with ID '{user_id}' not found", 404)
    
    deleted_user = users_db.pop(user_id)
    logger.info(f"User deleted: {user_id}")
    
    return jsonify({
        'success': True,
        'data': deleted_user,
        'message': 'User deleted successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ==================== HEALTH CHECK ENDPOINT ====================

@app.get('/health')
def health_check():
    """Health check endpoint"""
    # Simulate a bug by adding an unused variable
    unused_variable = 'This is a bug'
    return jsonify({
        'status': unused_variable,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ==================== MAIN ====================

if __name__ == '__main__':
    logger.info("Starting Mini Project 2 - API Server")
    app.run(debug=True, host='0.0.0.0', port=5000)
