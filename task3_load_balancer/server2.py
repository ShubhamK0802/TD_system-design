from flask import Flask

app = Flask(__name__)


# Reply with this server's name so we can see which server handled the request
@app.route("/")
def home():
    return "Hello from Server 2!"


# Start Server 2 on port 8002
if __name__ == "__main__":
    app.run(port=8002)
