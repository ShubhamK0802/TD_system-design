from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# Characters used to build short IDs (10 digits + 26 lowercase + 26 uppercase = 62)
CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Dictionary to store short_id -> long_url
url_store = {}

# Counter that gives every new URL a unique number
counter = 1


# Convert a number into a Base62 string (e.g. 62 -> "10")
def base62_encode(number):
    result = ""
    while number > 0:
        result = CHARACTERS[number % 62] + result  # Take the last digit and add it to the front
        number = number // 62                     # Remove the last digit
    return result


# API 1: Take a long URL and return a short ID
@app.route("/shorten", methods=["POST"])
def shorten():
    global counter

    data = request.get_json(silent=True)  # Read the JSON body (None if the JSON is broken)
    long_url = data.get("url") if data else None  # Get the URL from the body

    if not long_url:  # Return an error if no URL was sent
        return jsonify({"error": "Please send a url"}), 400

    short_id = base62_encode(counter)  # Turn the counter into a short ID
    url_store[short_id] = long_url     # Save the mapping in the dictionary
    counter = counter + 1              # Increase counter for the next URL

    return jsonify({"short_id": short_id, "short_url": "http://127.0.0.1:5000/" + short_id})


# API 2: Take a short ID and redirect to the original URL
@app.route("/<short_id>", methods=["GET"])
def go_to_url(short_id):
    long_url = url_store.get(short_id)  # Look up the original URL

    if long_url is None:  # Return an error if the short ID does not exist
        return jsonify({"error": "Short URL not found"}), 404

    return redirect(long_url)  # Send the user to the original URL


# Start the server on port 5000
if __name__ == "__main__":
    app.run(port=5000, debug=True)
