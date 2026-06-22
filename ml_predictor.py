import joblib
import pandas as pd

model = joblib.load("threat_model.pkl")

type_map = {
    "VEHICLE": 0,
    "DRONE": 1,
    "MISSILE": 2
}

def predict_threat(intruder, base_x, base_y):

    if intruder is None:
        return "NONE"

    distance = (
        ((intruder.x - base_x) ** 2) +
        ((intruder.y - base_y) ** 2)
    ) ** 0.5

    data = pd.DataFrame(
        [[
            type_map.get(
                intruder.intruder_type,
                0
            ),
            intruder.speed,
            distance
        ]],
        columns=[
            "Type",
            "Speed",
            "DistanceToBase"
        ]
    )

    prediction = model.predict(data)
    probabilities = model.predict_proba(data)

    confidence = max(probabilities[0]) * 100

    return prediction[0], confidence  