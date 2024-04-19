FROM python:3.x

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000 # Replace with your desired port

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]