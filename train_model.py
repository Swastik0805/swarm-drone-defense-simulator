import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load Dataset
df = pd.read_csv("threat_dataset.csv")

# Create Threat Labels
def classify(score):

    if score < 80:
        return "LOW"

    elif score < 140:
        return "MEDIUM"

    elif score < 200:
        return "HIGH"

    else:
        return "CRITICAL"

df["ThreatLevel"] = df["ThreatScore"].apply(classify)

# Encode Intruder Type
type_map = {
    "VEHICLE": 0,
    "DRONE": 1,
    "MISSILE": 2
}

df["Type"] = df["Type"].map(type_map)

# Features
X = df[
    [
        "Type",
        "Speed",
        "DistanceToBase"
    ]
]

# Target
y = df["ThreatLevel"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Model Accuracy: {accuracy*100:.2f}%")

# Save Model
joblib.dump(
    model,
    "threat_model.pkl"
)

print("Model saved successfully.")