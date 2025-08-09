
import os
import numpy as np
from .rf_model import RFWrapper
from .nn_model import NNWrapper
from .features import build_features, build_labels_from_signals, FEATURE_COLUMNS

class ModelManager:
    def __init__(self, model_type: str = "RF"):
        self.model_type = model_type.upper()
        self.model = RFWrapper() if self.model_type == "RF" else NNWrapper()

    def train(self, df, signals):
        X = build_features(df).values
        y = build_labels_from_signals(signals).values
        self.model.fit(X, y)

    def predict(self, df_row):
        X = df_row[FEATURE_COLUMNS].values.reshape(1, -1)
        pred = self.model.predict(X)[0]
        # map back {0,1,2} -> {hold,buy,sell} -> {-1,0,1} mapping inverse
        inv = {0:0, 1:1, 2:2}
        return pred

    def proba(self, df_row):
        X = df_row[FEATURE_COLUMNS].values.reshape(1, -1)
        return self.model.proba(X)[0]

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)

    def load(self, path):
        self.model.load(path)
