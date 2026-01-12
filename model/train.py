import os
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import accuracy_score, multilabel_confusion_matrix
import numpy as np

from data.preprocess import get_train_test_data
from model.architecture import build_lstm_model
from config.settings import LOGS_PATH, MODEL_PATH, EPOCHS


def train_model():
    print("📦 Cargando datos...")
    X_train, X_test, y_train, y_test = get_train_test_data()

    print("🧠 Construyendo modelo...")
    model = build_lstm_model()

    tb_callback = TensorBoard(log_dir=LOGS_PATH)

    print("🔥 Entrenando modelo...")
    model.fit(
        X_train,
        y_train,
        epochs=EPOCHS,
        callbacks=[tb_callback]
    )

    print("💾 Guardando modelo...")
    model.save(MODEL_PATH)

    print("📊 Evaluando modelo...")
    yhat = model.predict(X_test)

    ytrue = np.argmax(y_test, axis=1)
    ypred = np.argmax(yhat, axis=1)

    print(multilabel_confusion_matrix(ytrue, ypred))
    print("Accuracy:", accuracy_score(ytrue, ypred))
