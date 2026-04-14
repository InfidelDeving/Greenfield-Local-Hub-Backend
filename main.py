from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user_router

app = FastAPI()


app.include_router(
    user_router,
    prefix="/user",
    tags=["User"]
)

@app.get("/")
def default_route():
    return {"server status" : "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)



