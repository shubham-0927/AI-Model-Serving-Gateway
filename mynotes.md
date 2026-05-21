# MYNotes

## Correction or update
* make matrixes like failure, latency,etc.for evaluation
* change database secret key(from supersecretkey) in .env
* for email should we apply email checking logic at schema defination or define rules at the 
* in session.py need 
```

# Import all models to register them with Base.metadata
# This ensures the engine knows about all tables and relationships
from app.models.user import User
from app.models.api_key import APIKey
from app.models.job import Job
```
**else getting error while submitting the job to celery**: error was foreign key not found or table not found 


* In sse streaming :
    Right now: stream ignores disconnects
    Later: detect client disconnect, cleanup resources

* for request log starting with direct DB logging
later optimize with Redis batching  
    - DONE now, every 1st stage in redis then every 10 sec flsuh to postgres
    - But need somthing threshold for pushing the containts into postregress cant just let the cpu run for nothing like flush and do counting if redis have some data and when data crosses threshhold push or when timeout push it into db. 


*   middleware becomes useful for:
    Global request processing
    Examples:
    request IDs
    centralized logging
    CORS
    tracing
    timing
    metrics
    correlation IDs

* Production code has tests. Use FastAPI TestClient. Add pytest

* Streaming response not increasing the token used count?
* To GPT: you used http not https? also many other significant mistake that are really very degarous
        also why environment:
            POSTGRES_DB: aigateway
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
        password is open shoudnt we secure it????????????????

        also using  ports:
            - "80:80"
        require root permissions i guess then why ?

* there could be many kind of timeouts that needs to be implemented.
* routing logic right now is local memory based need redis-backed counters and distributed coordination
* in **routing** BETTER future evolution
```        Later:
        {
        "constraints": {
            "max_cost": 0.01,
            "max_latency_ms": 2000
        }
        }and gateway intelligently decides
```
* in gateway need to fix the token used count its always 50

* In round robin ⚠️ One Important Note

            Currently using: rate_limit_redis  , for routing state is okay.
            Later: you may want:orchestration_redis 
            separate logical namespace.But current stage is fine.


* system can handle model fails. and route to next model

* move to:✅ dynamic provider registry architecture (go to chat it is better there with many points such as extensibility)
* if provider["failure_count"] >= 3: this i dont want static threshold also once i got marked unhealthy then when it mark back healthy if user is not specifying the models


* right now logging only to terminal use some filesystem or db to store the logs (for error checking and traceback)

* **imp** need to remove the failing logic in openai provider code.
* Update the routing thresholds from fix developer define numbers to provider specific or use some ML model to learn the trend and update the thresholds.
## Implemention Notes


## sesion.py
* to work with relational databases python has toolkit (SQLAlchemy) to perform CRUD operation using python class and objects
    - SessionLocal = sessionmaker(
            autocommit = False,  // dont commit the python database model class or object data automatically, it help when working with large complex system
            //Unit of Work Pattern: It uses a "Session" to track changes to your objects. Changes aren't sent to the database until you explicitly "commit" them, which helps maintain data integrity across complex transactions.


            autoflush= False,
            bind = engine)


## models:
*   declarative_base is a factory function in SQLAlchemy that constructs a base class for ORM models
* uuid 1,2,3 ,4?
    - 1, 2, uses system info
    - 3 take some input and generate the using id using md5 (not very collision free)
    - 4 uses **psuedo-random** numbers

## authetication or jwt token verifcation
* in app/core/depencies there is a function get_current_user which cheks for the token sent by the user verify it using the secret if it is altered or something.

* creating access token using JWT that inputs expiry,secret key for signature, algorithm specification

## APIKeys
* usiing sha256 and intial 4 letters for storing the APIKeys
    purpose: sha256 exact match, and initial 4 letters fast loopup

* 3 layer checking : Prefix → fast DB lookup;Hash → secure verification;No plaintext storage

## Rate Limiting
* not using postgress, as need **high frequency ,small & atomic operations, low latency**
* Redis default port 6379
* Q.Why redis://localhost:6379/0? What is /0?
    👉 That /0 is the Redis database index.

## celery workers
* **important** need to run celery workers: 
```
celery -A app.workers.celery_app worker --loglevel=info
```
* Celery Architecture
    -  Your flow currently is:
    - Client → FastAPI → Redis Queue → Celery Worker → Execute Task
    - When you call:
```{py}
        process_job.delay(job.id)
```
        Celery:
        serializes task
        pushes it into Redis queue
        worker process picks task
        executes task

    - Celery uses: **multiprocessing pool (prefork)** NOT threads.

* **Why multiprocessing instead of threads**?

    - Because many Celery tasks are:
    - CPU-heavy : long-running 👉 **multiprocessing** bypasses Python GIL

## SSE (Server Stream Event):
*  To stream data to the client, it is one-way like webhooks but statefull remember previous state.
*   Also support automatic reconnection and FASTAPI implements 15 sec ping to chek connection alive or not.

## Redis for provider and model info
* IMPORTANT Architecture Principle
```
Separate:
 | Type                        | Storage       |
| --------------------------- | ------------- |
| static metadata             | Python config |
| runtime orchestration state | Redis         |
```
* metadata changes rarely, health changes constant (Different data lifecycles.)

## For health check and provider score
* using EMA(Exponential Moving Average)
* score = success/latency(current)
- **Problem** with this score:
    -   fastest provider may be expensive
    -   cheapest provider may be unreliable
    -   most reliable provider may be slower
* using weighted score:latency_weight = 0.5, reliability_weight = 0.3, cost_weight = 0.2
* using user tier aware weighting but later can use matrix factorizations to have personalization routing

## circuit breakers 
* for failer mitigation
* **circuit breaker pattern**:
```
| State     | Meaning          |
| --------- | ---------------- |
| CLOSED    | provider healthy |
| OPEN      | provider blocked |
| HALF_OPEN | testing recovery |
```
*When HALF_OPEN: allow only few test requests: VERY important


## exponential back-off
* if failure happen (dont spam retries)
```
fail
wait 200ms
retry

fail
wait 400ms
retry

fail
wait 800ms
```
* add jitter with delay, wait for delay+jitter(a random nouce) time
    - it prevent **Thunderaing herd problem**(when many clients try to reattempt at the same time (simultaneuosly) cause outrage again at the server)

## backpressure engineering
* when system pressure( the gateway's pressure) becomes to high, gracefully reject or throttle requests.
* use **Admission Control**

## Bacground Scheduler
* using redis queues: premium(higher priority), free(lower priority)
* Worker pulls:
    highest-priority requests first
    when capacity available
* 

## TO Run:
* Run once for db/init 
```
python3 -c "from app.db.init_db import init_db; init_db()"

```

```
uvicorn app.main:app --reload
```
to check database for me only(private):
```
psql -h localhost -U postgres -d aigateway
```
* to run workers:
```
celery -A app.workers.celery_app worker --loglevel=info
celery -A app.workers.celery_app beat --loglevel=info
```
* swagger UI to check the streaming response:
```
curl -N \
-H "Authorization: Bearer sk-xxxx" \
http://127.0.0.1:8000/v1/stream/completions
```
* check redis and provider health
```
docker compose exec redis redis-cli
```

### to test :
* the endpoints:
```
{
  "provider": "openai",
  "strict_provider": false,
  "prompt": "hello"
}
```
## to visualize
* prometheus:
```
http://localhost:9090/
```
* grafana:
```
localhost:3000
```

* jeager:
```
http://localhost:16686
```
* metrics:
```
http://localhost/metrics
```


### to start project in docker:
```
docker compose build
docker compose up
docker compose up --build
docker compose exec api python -c "from app.db.init_db import init_db; init_db()"

docker compose down
```
## database:
from ire assigment "Indexing an retrieval"
def __init__(self, version="selfindex", user="postgres", password="postgres", host="localhost")

* psql -h localhost -U postgres -d aigateway (for password postgres)
* to drop tables:
```
DROP TABLE jobs;
DROP TABLE api_keys;
DROP TABLE users;
```

## Docker 
* to check docker running:
```
systemctl status docker
```
* to start docker:
```
sudo systemctl start docker

docker compose up --build
```

* to check running containers:
```
docker compose ps
```

## Nginx
* why:
```
events {
    worker_connections 1024;
}
```
    -   worker_connections 1024: This sets the maximum number of simultaneous open connections that a single worker process can maintain at any given moment.
* 