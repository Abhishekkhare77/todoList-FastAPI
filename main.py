from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as list_router

config = dotenv_values(".env")

app = FastAPI(
    title="Todo List API",
    description="A simple Todo List API using FastAPI and MongoDB",
    version="0.1.0",
    redoc_url=None,
    docs_url="/",
    openapi_url="/openapi.json",
    contact={
        "name": "Abhishek khare",
        "url": "https://github.com/Abhishekkhare77"
    }
)

allowed_origins = ["*"]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specify the allowed origins
    allow_credentials=True,  # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "Todo List API using Fast API and pymongo"}

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(list_router, tags=["list"], prefix="/list")

