from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemyimport create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.context import CryptContext
from bcrypt import hashpw, gensalt, checkpw
from prometheus_fastapi_instrumentator import Instrumentator

# Database Configuration
DATABASE_URL = "mysql://user:password@host/database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def set_password(self, password):
        self.hashed_password = hashpw(password, gensalt())

    def verify_password(self, password):
        return checkpw(password, self.hashed_password)

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2 Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ... (Registration route, Login route, Protected route, Health check)

# Prometheus Metrics Setup
metrics = PrometheusMetrics(app)
metrics.info(
    "app_info",
    "Application info, version and start time",
    version="0.1.0",
    start_time=datetime.datetime.now(),
)
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        metrics.register_error.labels(endpoint="register").inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        metrics.register_error.labels(endpoint="register").inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    # Create new user and set password
    new_user = User(username=user.username, email=user.email)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    metrics.register_success.labels(endpoint="register").inc()
    return {"message": "User registered successfully"}

# Login Route
@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.username == user.username).first()
    if not user:
        metrics.register_error.labels(endpoint="register").inc()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Verify password
    if not user.verify_password(user.password):
        metrics.register_error.labels(endpoint="register").inc()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Generate token
    token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
    metrics.register_success.labels(endpoint="register").inc()
    return {"message": "Login successful", "token": token}

# Protected Route (Example)
@app.get("/protected", status_code=status.HTTP_200_OK)
async def protected_route(current_user: User = Depends(oauth2_scheme)):
    return {"message": f"Welcome, {current_user.username}!"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

# Prometheus Integration
Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
