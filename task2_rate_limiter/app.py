import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Maximum number of requests allowed per user
MAX_REQUESTS = 5

# Time window in seconds (1 minute)
TIME_WINDOW = 60

# Dictionary to store user_id -> list of request timestamps
user_requests = {}


# Check if a user is allowed to make a request
def is_allowed(user_id):
    now = time.time()  # Current time in seconds

    if user_id not in user_requests:  # First request from this user
        user_requests[user_id] = []

    # Keep only the timestamps from the last 60 seconds
    recent = []
    for t in user_requests[user_id]:
        if now - t < TIME_WINDOW:
            recent.append(t)
    user_requests[user_id] = recent

    if len(recent) >= MAX_REQUESTS:  # User already made 5 requests in the last minute
        return False

    user_requests[user_id].append(now)  # Save this request's timestamp
    return True


# API: Return some data, but only if the user is under the limit
@app.route("/data", methods=["GET"])
def get_data():
    user_id = request.args.get("user_id", request.remote_addr)  # Use ?user_id=... or the user's IP address

    if not is_allowed(user_id):  # Block the user if they crossed the limit
        return jsonify({"error": "Too Many Requests: Try again later."}), 429

    count = len(user_requests[user_id])  # How many requests the user has made in this minute
    return jsonify({"message": "Here is your data!", "user_id": user_id, "requests_used": count})


# Start the server on port 5001
if __name__ == "__main__":
    app.run(port=5001, debug=True)
