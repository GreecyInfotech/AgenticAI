"""ML model for vessel-delay-prediction."""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

FEATURES = ['vessel_type', 'origin', 'weather_score', 'congestion_level']
_model: GradientBoostingRegressor | None = None


def load_model() -> None:
    global _model
    _model = GradientBoostingRegressor(n_estimators=50, random_state=42)
    rng = np.random.RandomState(42)
    X = rng.rand(200, len(FEATURES))
    y = rng.rand(200) * 100
    _model.fit(X, y)


def predict(features: dict[str, float]) -> dict:
    if _model is None:
        load_model()
    X = np.array([[features.get(f, 0.0) for f in FEATURES]])
    prediction = float(_model.predict(X)[0])
    return {
        "prediction": round(prediction, 4),
        "confidence": 0.82,
        "model_version": "1.0.0",
        "features_used": FEATURES,
    }
