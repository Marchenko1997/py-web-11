from fastapi import FastAPI
from src.routes import contacts

app = FastAPI()
app.include_router(contacts.router)


@app.get("/")
def root():
    return {"message": "Contact API is running"}
