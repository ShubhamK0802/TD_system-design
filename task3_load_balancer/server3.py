from flask import Flask

app = Flask(__name__)


# Reply with this server's name so we can see which server handled the request
@app.route("/")
def home():
    return "Hello from Server 3!"


# Start Server 3 on port 8003
if __name__ == "__main__":
    app.run(port=8003)
