from fastapi import FastAPI, Body, HTTPException
import redis
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Summary, Histogram

app = FastAPI()

# Prometheus Metrics Setup
DB_QUERY_TIME = Summary('redis_query_time_seconds', 'Time spent interacting with Redis')
DB_CONNECTIONS = Counter('redis_connections_total', 'Total number of Redis connections') # Not strictly a connection, but tracks interactions
Instrumentator().instrument(app).expose(app) 

# Request Latency
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Distribution of request latencies', buckets=[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, float("inf")])

# Connect to Redis 
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Helper Functions with Metrics
@REQUEST_LATENCY.time()
def get_employee_data(employee_id):
    DB_CONNECTIONS.inc()
    data = redis_client.get(employee_id)
    if data:
        return data.decode('utf-8')
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

def store_employee_data(employee_id, data):
    DB_CONNECTIONS.inc()
    redis_client.set(employee_id, data)

# Routes (Mostly the same)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@REQUEST_LATENCY.time()
@app.get("/employees")
async def get_employees():
    # For simplicity, assuming you fetch employee IDs from somewhere else
    employee_ids = [1, 2, 3, ...]

    employees = []
    for employee_id in employee_ids:
        data = get_employee_data(employee_id)
        if data: # Only add employee if data was found in Redis
            employees.append(json.loads(data)) # Convert JSON string to dictionary

    return {'employees': employees}
@REQUEST_LATENCY.time()
@app.post("/employees")
async def create_employee(employee_data: dict = Body(...)):
    # Basic Input Validation
    if "id" not in employee_data:
        raise HTTPException(status_code=400, detail="Employee data must include an 'id' field")

    employee_id = employee_data["id"]

    # Check if employee already exists
    existing_data = get_employee_data(employee_id)
    if existing_data:
        raise HTTPException(status_code=409, detail="Employee with this ID already exists")

    # Store the data (as JSON)
    store_employee_data(employee_id, json.dumps(employee_data))
    return {"message": "Employee created successfully"}
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}