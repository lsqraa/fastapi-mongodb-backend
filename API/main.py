from fastapi import FastAPI #pip install "fastapi[all]""
from routers import products, users_db, jwt_auth_users
from fastapi.staticfiles import StaticFiles
app = FastAPI()

#routers

app.include_router(products.router)
app.include_router(users_db.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name= "static")

#initialize server whit uvicorn main:app --reload
@app.get("/")
async def root ():
    return "Hola Mundo"

@app.get("/url")
async def url ():
    return {"url_curso":"https://mouredev.com/python"}


