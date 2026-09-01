from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.feature_flag import FlagEvaluationRequest
from app.services.flag_evaluation import evaluate_flag
from app.core.security import get_current_user


router = APIRouter(
    prefix="/flags",
    tags=["Flag Evaluation"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/evaluate")
def evaluate_feature_flag(
    request: FlagEvaluationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        value = evaluate_flag(
            db,
            request.flag_key,
            request.environment
        )

        return {
            "flag_key": request.flag_key,
            "value": value
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )