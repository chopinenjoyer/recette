from fastapi import Depends, HTTPException, status
from app.core.security import verify_token

def get_current_user(token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token