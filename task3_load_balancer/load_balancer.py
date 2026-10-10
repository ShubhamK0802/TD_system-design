import requests
from flask import Flask

app = Flask(__name__)

# List of backend servers the load balancer can send requests to
SERVERS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003",
]

# Index of the server that will get the next request
current = 0


# Pick the next server in order (1 -> 2 -> 3 -> back to 1)
def get_next_server():
    global current
    server = SERVERS[current]                # Take the server at the current position
    current = (current + 1) % len(SERVERS)   # Move to the next one, wrap to 0 after the last
    return server


# Every request to the load balancer is forwarded to one backend server
@app.route("/")
def forward_request():
    server = get_next_server()  # Choose a server using Round Robin

    try:
        response = requests.get(server, timeout=3)  # Forward the request to the chosen server
        print("Forwarded to", server, "->", response.text)  # Log which server answered
        return response.text, response.status_code  # Send the server's reply back to the user
    except requests.exceptions.RequestException:
        return "Server " + server + " is not available", 503  # Server is down or not responding


# Start the load balancer on port 8000
if __name__ == "__main__":
    app.run(port=8000)
