
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np

class RFWrapper:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def proba(self, X):
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        # fallback uniform
        n = len(X)
        return np.ones((n,3)) / 3.0

    def save(self, path):
        joblib.dump(self.model, path)

    def load(self, path):
        self.model = joblib.load(path)
