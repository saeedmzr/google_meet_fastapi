from fastapi import FastAPI
from app.routes import auth, events
from app.database.session import engine, Base

app = FastAPI()

# Include routes
app.include_router(auth.router)
app.include_router(events.router)

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)