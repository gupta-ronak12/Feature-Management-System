from sqlalchemy.orm import Session

from app.models.feature_flag import FeatureFlag
from app.models.environment import Environment
from app.models.environment_override import EnvironmentOverride



def evaluate_flag(
    db: Session,
    flag_key: str,
    environment: str,
    user_context: dict | None = None
):
    # Find the feature flag
    flag = db.query(FeatureFlag).filter(
        FeatureFlag.key == flag_key
    ).first()

    if not flag:
        raise ValueError("Feature flag not found")

    # Find the environment
    env = db.query(Environment).filter(
        Environment.name == environment
    ).first()

    if not env:
        raise ValueError("Environment not found")

    # If the flag is globally disabled, return False
    if not flag.enabled:
        return False

    # Check for an environment-specific override
    override = db.query(EnvironmentOverride).filter(
        EnvironmentOverride.flag_id == flag.id,
        EnvironmentOverride.environment_id == env.id
    ).first()

    if override:
        return override.value

    # No override found, so use the default value
    return flag.default_value