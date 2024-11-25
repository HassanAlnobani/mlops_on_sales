"""
app.py
======
This Flask app provides a REST API endpoint for product recommendations with caching capabilities.
"""

from flask import Flask, request, jsonify  # Flask components for handling requests and responses
from flask_caching import Cache           # Flask-Caching for response caching
import logging                             # Module for logging API activity

# Initialize the Flask app
app = Flask(__name__)

# Configure caching (using in-memory cache)
app.config['CACHE_TYPE'] = 'SimpleCache'      # Other options: RedisCache, MemcachedCache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300    # Cache timeout in seconds (5 minutes)
cache = Cache(app)                            # Initialize caching for the app

# Predefined static product recommendations
recommended_product_ids = [1, 2, 3]

# Configure logging to record API requests and responses
logging.basicConfig(filename="service.log", level=logging.INFO)

@app.route('/recommend', methods=['POST'])
@cache.cached(query_string=True)  # Cache the response based on request payload
def recommend():
    """
    POST Endpoint: /recommend
    --------------------------
    Simulates product recommendations for a given product. Responses are cached to improve performance.

    Request:
        - Expects a JSON payload with a "product_id" key.

    Response:
        - If "product_id" is provided, returns the static list of recommendations.
        - If "product_id" is missing, returns an error message with status 400.

    Caching:
        - The response for identical requests is cached for 5 minutes.
    """
    # Extract JSON data from the request
    data = request.json

    # Retrieve the "product_id" from the request
    product_id = data.get("product_id")

    # Validate the input: Ensure "product_id" is provided
    if not product_id:
        # Respond with an error if "product_id" is missing
        return jsonify({"error": "Product ID is required"}), 400

    # Log the received request
    logging.info(f"Received request for Product ID: {product_id}")

    # Create a response with static recommendations
    response = {"product_id": product_id, "recommended_product_ids": recommended_product_ids}

    # Log the response
    logging.info(f"Response: {response}")

    # Return the response as JSON
    return jsonify(response)

if __name__ == "__main__":
    """
    Main entry point for running the Flask app.
    - Starts the app in debug mode.
    """
    app.run(debug=True, host="0.0.0.0", port=5000)
