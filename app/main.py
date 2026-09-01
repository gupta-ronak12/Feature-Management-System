from fastapi import FastAPI
from app.routers.feature_flags import router as feature_flags_router
from app.routers.auth import router as auth_router
from app.routers.environment_override import router as environment_override_router
from app.routers import flag_evaluation
from app.routers import environments

app = FastAPI(
    title="Feature Management System",
    description="Web-based Feature Flag Management System with Release Control Assistance",
    version="1.0.0",
)
app.include_router(feature_flags_router)
app.include_router(auth_router)
app.include_router(environment_override_router)
app.include_router(flag_evaluation.router)
app.include_router(environments.router)
@app.get("/")
def root():
    return {"message": "Feature Management System API is running"}
