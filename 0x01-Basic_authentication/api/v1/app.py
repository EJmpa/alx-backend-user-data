#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from werkzeug.exceptions import HTTPException
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def request_unauthorized(error) -> tuple:
    """Return a JSON response for a 401 error.

    Args:
        error: The error that occurred.

    Returns:
        A tuple containing the JSON response and the HTTP status code.
    """
    return jsonify({'error': 'Unauthorized'}), 401


@app.errorhandler(403)
def forbidden(error: HTTPException) -> tuple:
    """Handle 403 errors by returning a JSON response.

    Args:
        error: The error that occurred.

    Returns:
        A tuple containing the JSON response and the HTTP status code.
    """
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
