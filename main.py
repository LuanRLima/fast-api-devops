from fastapi import FastAPI
import mysql.connector
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Summary

app = FastAPI()

DB_QUERY_TIME = Summary('db_query_time_seconds', 'Time spent executing database queries')
DB_CONNECTIONS = Counter('db_connections_total', 'Total number of database connections')
DB_LAST_CONNECTION = Summary('db_last_connection_seconds', 'Time since last database connection')
# Prometheus Instrumentation
Instrumentator().instrument(app).expose(app)


@DB_LAST_CONNECTION.time()
@app.get("/")
async def root():
    DB_CONNECTIONS.inc()  # Increment DB connections counter
    return {"message": "Hello World"}

@DB_LAST_CONNECTION.time()
@app.get("/employees")
async def get_employees():
    print('DB connecting')
    connection = mysql.connector.connect(
        user='root',
        password='RootPassword',
        host='mysql',
        port='3306',
        database='Company'
    )
    print('DB connected')

    cursor = connection.cursor(dictionary=True)
    DB_CONNECTIONS.inc()  # Increment DB connections counter
    DB_QUERY_TIME.time()
    cursor.execute('Select * FROM employees')
    employees = cursor.fetchall()
    datas = []
    for employee in employees:
        print(employee)
        data = {
            "first_name": employee["first_name"],
            "last_name": employee["last_name"],
            "email": employee["email"],
            "department": employee["department"]
        }
        datas.append(data)
    connection.close()
    print('DB closed')
    return {'employees': datas}

@DB_LAST_CONNECTION.time()
@app.get("/healthcheck")
def healthcheck():
    DB_CONNECTIONS.inc()
    return {"status": "ok"}


@app.get("/metrics")
def export_metrics():
    return generate_latest()