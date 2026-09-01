from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.feature_flag import FeatureFlag
from app.schemas.feature_flag import (
    FeatureFlagCreate,
    FeatureFlagUpdate,
    FeatureFlagResponse
)
from app.core.security import get_current_user


router = APIRouter(
    prefix="/feature-flags",
    tags=["Feature Flags"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE FEATURE FLAG
@router.post("/", response_model=FeatureFlagResponse)
def create_feature_flag(
    feature_flag: FeatureFlagCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_flag = db.query(FeatureFlag).filter(
        FeatureFlag.key == feature_flag.key
    ).first()

    if existing_flag:
        raise HTTPException(
            status_code=400,
            detail="Feature flag with this key already exists"
        )

    new_flag = FeatureFlag(**feature_flag.model_dump())

    db.add(new_flag)
    db.commit()
    db.refresh(new_flag)

    return new_flag


# GET ALL FEATURE FLAGS
@router.get("/", response_model=list[FeatureFlagResponse])
def get_feature_flags(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(FeatureFlag).all()


# GET FEATURE FLAG BY ID
@router.get("/{flag_id}", response_model=FeatureFlagResponse)
def get_feature_flag(
    flag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    feature_flag = db.query(FeatureFlag).filter(
        FeatureFlag.id == flag_id
    ).first()

    if not feature_flag:
        raise HTTPException(
            status_code=404,
            detail="Feature flag not found"
        )

    return feature_flag


# UPDATE FEATURE FLAG
@router.put("/{flag_id}", response_model=FeatureFlagResponse)
def update_feature_flag(
    flag_id: int,
    feature_flag: FeatureFlagUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_flag = db.query(FeatureFlag).filter(
        FeatureFlag.id == flag_id
    ).first()

    if not existing_flag:
        raise HTTPException(
            status_code=404,
            detail="Feature flag not found"
        )

    update_data = feature_flag.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_flag, key, value)

    db.commit()
    db.refresh(existing_flag)

    return existing_flag


# DELETE FEATURE FLAG
@router.delete("/{flag_id}")
def delete_feature_flag(
    flag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    feature_flag = db.query(FeatureFlag).filter(
        FeatureFlag.id == flag_id
    ).first()

    if not feature_flag:
        raise HTTPException(
            status_code=404,
            detail="Feature flag not found"
        )

    db.delete(feature_flag)
    db.commit()

    return {
        "message": "Feature flag deleted successfully"
    }