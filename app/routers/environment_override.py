from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.environment_override import EnvironmentOverride
from app.models.feature_flag import FeatureFlag
from app.models.environment import Environment
from app.schemas.environment_override import (
    EnvironmentOverrideCreate,
    EnvironmentOverrideResponse
)
from app.core.security import get_current_user


router = APIRouter(
    prefix="/environment-overrides",
    tags=["Environment Overrides"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE / UPDATE ENVIRONMENT OVERRIDE
@router.post("/", response_model=EnvironmentOverrideResponse)
def create_environment_override(
    override: EnvironmentOverrideCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if feature flag exists
    feature_flag = db.query(FeatureFlag).filter(
        FeatureFlag.id == override.flag_id
    ).first()

    if not feature_flag:
        raise HTTPException(
            status_code=404,
            detail="Feature flag not found"
        )

    # Check if environment exists
    environment = db.query(Environment).filter(
        Environment.id == override.environment_id
    ).first()

    if not environment:
        raise HTTPException(
            status_code=404,
            detail="Environment not found"
        )

    # Check if override already exists
    existing_override = db.query(EnvironmentOverride).filter(
        EnvironmentOverride.flag_id == override.flag_id,
        EnvironmentOverride.environment_id == override.environment_id
    ).first()

    if existing_override:
        existing_override.value = override.value
        db.commit()
        db.refresh(existing_override)

        return existing_override

    # Create new override
    new_override = EnvironmentOverride(
        flag_id=override.flag_id,
        environment_id=override.environment_id,
        value=override.value
    )

    db.add(new_override)
    db.commit()
    db.refresh(new_override)

    return new_override


# GET ENVIRONMENT OVERRIDE
@router.get("/{flag_id}/{environment_id}")
def get_environment_override(
    flag_id: int,
    environment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if feature flag exists
    feature_flag = db.query(FeatureFlag).filter(
        FeatureFlag.id == flag_id
    ).first()

    if not feature_flag:
        raise HTTPException(
            status_code=404,
            detail="Feature flag not found"
        )

    # Find environment override
    override = db.query(EnvironmentOverride).filter(
        EnvironmentOverride.flag_id == flag_id,
        EnvironmentOverride.environment_id == environment_id
    ).first()

    # If override exists, return it
    if override:
        return {
            "flag_id": flag_id,
            "environment_id": environment_id,
            "value": override.value,
            "source": "environment_override"
        }

    # Otherwise use default value
    return {
        "flag_id": flag_id,
        "environment_id": environment_id,
        "value": feature_flag.default_value,
        "source": "default_value"
    }