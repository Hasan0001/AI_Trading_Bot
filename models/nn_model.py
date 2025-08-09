
import tensorflow as tf
from tensorflow import keras

def build_nn(input_dim=20, out_dim=3):
    model = keras.Sequential([
        keras.layers.Input(shape=(input_dim,)),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(out_dim, activation="softmax"),
    ])
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss=keras.losses.SparseCategoricalCrossentropy(),
                  metrics=["accuracy"])
    return model

class NNWrapper:
    def __init__(self):
        self.model = build_nn()

    def fit(self, X, y):
        es = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
        self.model.fit(X, y, validation_split=0.2, epochs=50, batch_size=32, callbacks=[es], verbose=0)

    def predict(self, X):
        probs = self.model.predict(X, verbose=0)
        return probs.argmax(axis=1)

    def proba(self, X):
        return self.model.predict(X, verbose=0)

    def save(self, path):
        self.model.save(path)

    def load(self, path):
        self.model = keras.models.load_model(path)
