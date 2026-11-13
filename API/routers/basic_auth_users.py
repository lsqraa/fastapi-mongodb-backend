from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

class User(BaseModel):    
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Developer",
        "email": "alice@example.com",
        "disabled": False,
        "password": "secretpassword123"
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Inactive",
        "email": "bob@example.com",
        "disabled": True,
        "password": "secretpassword456"
    },
}


def search_user_db(username: str) -> UserDB | None:
    if username in users_db:
        return UserDB(**users_db[username])
    return None

def search_user(username: str) -> User | None:
    if username in users_db:
        return User(**users_db[username])
    return None


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Auth Credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario Inactivo"
        )
    return user


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
  
    user = search_user_db(form.username)
    
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario no es correcto"
        )

    if not form.password == user.password: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Contraseña Incorrecta"
        )

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
