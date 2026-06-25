import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext

# 1. SECURITY CONFIGURATION BASICS
SECRET_KEY = "SUPER_SECRET_SYSTEM_CRYPTOGRAPHIC_SIGNING_KEY" # In production, keep this hidden in a .env file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing configuration matrix
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Directs FastAPI to look for the security token in the standard HTTP "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Secured Enterprise Ingestion API")

# Mock User Database Store (Passwords stored as secure Bcrypt hashes)
MOCK_USER_DB = {
    "admin_worker": {
        "username": "admin_worker",
        "hashed_password": pwd_context.hash("production_secure_pass_123"),
        "disabled": False
    }
}

class TokenData(BaseModel):
    username: Optional[str] = None

class IngestionPayload(BaseModel):
    node_id: str
    status: str

# =====================================================================
# 2. CRYPTOGRAPHIC CRYPTO HELPER UTILITIES
# =====================================================================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Generates a transient, signed JWT infrastructure string."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Sign the token using our system key and hashing algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# =====================================================================
# 3. INTERCEPTOR DEPENDENCY (The Security Gate)
# =====================================================================
async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    """Decodes and validates the token. Rejects unauthorized traffic automatically."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate infrastructure access credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token cryptographically using our secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
        
    if username not in MOCK_USER_DB:
        raise credentials_exception
    return token_data

# =====================================================================
# 4. AUTHENTICATION & SECURED ENDPOINTS
# =====================================================================
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """The handshake gate. Validates credentials and delivers the security JWT."""
    user = MOCK_USER_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect internal username or password allocation.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/secure-metrics", status_code=201)
async def ingest_protected_metric(
    payload: IngestionPayload, 
    current_user: TokenData = Depends(get_current_active_user)
):
    """A completely secured network endpoint. Notice the 'Depends' security wall."""
    print(f"🔒 Authenticated request cleared for user: {current_user.username}")
    return {
        "status": "success",
        "message": f"Metrics secured for node [{payload.node_id}] via cryptographically verified channel."
    }
