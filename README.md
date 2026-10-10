# System Design Fundamentals with Python

A collection of three beginner-friendly system design projects built using Python and Flask. This repository demonstrates core backend concepts through practical implementations of URL shortening, API rate limiting, and load balancing.

## Projects Overview

| Project | Description | Key Concepts |
|---|---|---|
| URL Shortener Lite | Converts long URLs into short IDs and redirects users to the original URLs. | REST APIs, Base62 encoding, in-memory storage |
| Rate Limiter Mini | Restricts each user to five requests within a rolling 60-second window. | Sliding window, timestamps, HTTP 429 |
| Round-Robin Load Balancer | Distributes incoming requests across three backend servers in sequence. | Load balancing, round-robin algorithm, HTTP 503 |

## Tech Stack

- **Language:** Python 3.12
- **Web Framework:** Flask
- **HTTP Client:** Requests
- **Testing:** curl / curl.exe
- **Version Control:** Git and GitHub

## Repository Structure

```text
system-design/
├── task1_url_shortener/
│   ├── app.py
│   └── requirements.txt
├── task2_rate_limiter/
│   ├── app.py
│   └── requirements.txt
├── task3_load_balancer/
│   ├── server1.py
│   ├── server2.py
│   ├── server3.py
│   ├── load_balancer.py
│   └── requirements.txt
└── README.md
```

## 1. URL Shortener Lite

**Objective:** Build a lightweight service that generates short IDs for long URLs and redirects users to the original destination.

### How it works

- Accepts a long URL through a POST request.
- Generates a short ID using a counter and Base62 encoding.
- Stores the mapping between the short ID and the original URL in an in-memory dictionary.
- Redirects users when they visit the corresponding short URL.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/shorten` | Generate a short ID for a URL |
| GET | `/<short_id>` | Redirect to the original URL |

### Run locally

```powershell
cd task1_url_shortener
pip install -r requirements.txt
python app.py
```

The service runs on `http://127.0.0.1:5000`.

### Test the API

In Windows PowerShell 5.1 (the version included with Windows):

```powershell
curl.exe -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{\"url\":\"https://www.google.com\"}'
```

In PowerShell 7.3 or newer, or in macOS/Linux terminals, remove the backslashes:

```bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"url":"https://www.google.com"}'
```

Example response:

```json
{
  "short_id": "1",
  "short_url": "http://127.0.0.1:5000/1"
}
```

Open `http://127.0.0.1:5000/1` in a browser to be redirected to the original URL.

## 2. Rate Limiter Mini

**Objective:** Prevent excessive API requests by enforcing a per-user request limit.

### How it works

- Tracks request timestamps separately for each user.
- Removes timestamps older than 60 seconds.
- Allows up to five requests within the rolling window.
- Returns HTTP `429 Too Many Requests` when the limit has been reached.

### API Endpoint

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/data` | Return data if the user is within the rate limit |

### Run locally

```powershell
cd task2_rate_limiter
pip install -r requirements.txt
python app.py
```

The service runs on `http://127.0.0.1:5001`.

### Test the API

Send six requests in a row:

```powershell
1..6 | ForEach-Object { curl.exe -s "http://127.0.0.1:5001/data?user_id=alice"; "" }
```

Expected behavior:

- Requests 1–5: HTTP `200 OK`
- Request 6, while the previous five remain within the window: HTTP `429 Too Many Requests`

The user ID parameter is provided for demonstration and testing. If it is missing, the client's IP address is used.

## 3. Round-Robin Load Balancer

**Objective:** Distribute incoming requests across three backend servers using the round-robin algorithm.

### How it works

- Runs three independent Flask backend servers.
- Routes incoming requests to the next server in sequence.
- Uses the modulo operator to cycle back to the first server after the third.
- Applies a three-second timeout to backend requests.
- Returns HTTP `503 Service Unavailable` when the selected backend cannot be reached.

### Server Configuration

| Component | Port |
|---|---:|
| Load Balancer | 8000 |
| Backend Server 1 | 8001 |
| Backend Server 2 | 8002 |
| Backend Server 3 | 8003 |

### Run locally

Install the dependencies:

```powershell
cd task3_load_balancer
pip install -r requirements.txt
```

Open four separate terminals in the `task3_load_balancer` directory and run one command in each:

**Terminal 1**

```powershell
python server1.py
```

**Terminal 2**

```powershell
python server2.py
```

**Terminal 3**

```powershell
python server3.py
```

**Terminal 4**

```powershell
python load_balancer.py
```

### Test the load balancer

Send requests to:

```powershell
curl.exe http://127.0.0.1:8000/
```

Expected response sequence after a fresh start:

```text
Hello from Server 1!
Hello from Server 2!
Hello from Server 3!
Hello from Server 1!
```

## Key Learnings

- Designing basic HTTP API endpoints and handling appropriate status codes.
- Implementing Base62 encoding for compact URL identifiers.
- Managing request timestamps using a sliding-window rate-limiting approach.
- Distributing requests across multiple backend servers using round-robin scheduling.
- Handling backend connection failures and timeouts.
- Understanding the trade-offs of in-memory state in backend applications.

## Limitations and Future Improvements

These implementations focus on demonstrating fundamental concepts rather than production deployment.

Potential improvements include:

- **URL Shortener:** Persistent database storage, URL validation, and more difficult-to-guess identifiers.
- **Rate Limiter:** Shared storage such as Redis, authenticated user identification, and more efficient request tracking.
- **Load Balancer:** Health checks, automatic skipping of unhealthy servers, and support for additional HTTP methods.
- **All projects:** Automated tests, structured logging, configuration management, and containerization.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/ShubhamK0802/system-design.git
cd system-design
```

Follow the individual setup instructions in each project section to install dependencies and run the applications locally.

---

**Author:** Shubham Ramashankar Kanaujiya

**Repository:** [github.com/ShubhamK0802/system-design](https://github.com/ShubhamK0802/system-design)
