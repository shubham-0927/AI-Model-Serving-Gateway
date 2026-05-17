# AI Model Serving Gateway

A production-oriented AI Model Serving Gateway built with FastAPI and gRPC-inspired service orchestration concepts.
The system provides centralized API routing, authentication, rate limiting, load balancing, and model inference management for LLM-style services.

---

## Features

* FastAPI-based API Gateway
* API Key Authentication
* Tier-based Rate Limiting
* Multiple Load Balancing Policies

  * Round Robin
  * Least Load
  * Pick First
* Async Request Handling
* Backend Model Server Registration
* Health Monitoring
* Metrics Collection
* Scalable Microservice Architecture
* Docker-ready Structure
* Performance Testing Support

---

## Architecture

```text
                +-------------------+
                |      Client       |
                +---------+---------+
                          |
                          v
               +--------------------+
               |   API Gateway      |
               |  FastAPI Server    |
               +---------+----------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
   +-------------+ +-------------+ +-------------+
   | Backend 1   | | Backend 2   | | Backend N   |
   | Model Server| | Model Server| | Model Server|
   +-------------+ +-------------+ +-------------+
```

---

## Tech Stack

* Python
* FastAPI
* Uvicorn
* AsyncIO
* gRPC Concepts
* Docker
* Redis (optional for rate limiting/cache)
* Prometheus/Grafana (planned)

---

## Project Structure

```text
ai-model-serving-gateway/
│
├── gateway/
│   ├── main.py
│   ├── routes/
│   ├── auth/
│   ├── load_balancer/
│   ├── middleware/
│   └── utils/
│
├── backend/
│   ├── model_server.py
│   └── worker.py
│
├── tests/
│
├── performance/
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ai-model-serving-gateway.git
cd ai-model-serving-gateway
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Gateway

Start the FastAPI gateway:

```bash
uvicorn gateway.main:app --reload
```

The server will run at:

```text
http://127.0.0.1:8000
```

---

## API Example

### Completion Endpoint

```http
POST /completions
```

Request:

```json
{
  "prompt": "Explain transformers in deep learning",
  "max_tokens": 128
}
```

Response:

```json
{
  "response": "Transformers are neural network architectures..."
}
```

---

## Load Balancing Policies

| Policy      | Description                            |
| ----------- | -------------------------------------- |
| Round Robin | Cycles through servers sequentially    |
| Least Load  | Selects server with lowest active load |
| Pick First  | Always selects first healthy server    |

---

## Planned Features

* JWT Authentication
* Distributed Service Discovery
* Kubernetes Deployment
* Streaming Responses
* Request Queueing
* GPU-aware Scheduling
* Prometheus Metrics
* Grafana Dashboard
* OpenTelemetry Tracing
* Circuit Breakers
* Retry & Failover Logic

---

## Performance Goals

* Low-latency request routing
* Horizontal scalability
* Fault-tolerant backend handling
* Efficient async concurrency

---

## Future Improvements

* Multi-model routing
* Dynamic autoscaling
* Semantic caching
* Batch inference support
* Request prioritization
* Distributed tracing

---

## License

MIT License

---

## Author

Shubham Dewangan
