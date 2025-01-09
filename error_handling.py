from functools import wraps
from flask import render_template, jsonify

# General error handling decorator that catches all exceptions
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the error (you can expand this with more advanced logging)
            print(f"Error: {str(e)}")
            
            # Return a generic error page for all errors (500)
            return render_template('error.html', error_message=str(e)), 500
    return decorated_function

# Specific error handling for 404 (Page Not Found)
def handle_404_error(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html', error_message="Page Not Found"), 404

# Specific error handling for 500 (Internal Server Error)
def handle_500_error(app):
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html', error_message="Internal Server Error"), 500

# Example: Specific error handling for any type of validation errors or other errors
def handle_validation_error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400  # Return JSON for validation errors (400)
    return decorated_function
