import os
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import accuracy_score, multilabel_confusion_matrix
import numpy as np

from data.preprocess import get_train_test_data
from model.architecture import build_lstm_model
from config.settings import LOGS_PATH, MODEL_PATH


def train_model():
    print("📦 Cargando datos...")
    X_train, X_test, y_train, y_test = get_train_test_data()

    print("🧠 Construyendo modelo...")
    model = build_lstm_model()

    # Callbacks
    tb_callback = TensorBoard(log_dir=LOGS_PATH)

    print("early_stopping")
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )

    print("reduce_lr")
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )

    print("🔥 Entrenando modelo...")
    model.fit(
        X_train,
        y_train,
        epochs=200,
        validation_split=0.1,
        callbacks=[tb_callback, early_stop, reduce_lr]
    )

    print("💾 Guardando modelo...")
    model.save(MODEL_PATH)

    print("📊 Evaluando modelo...")
    yhat = model.predict(X_test)

    ytrue = np.argmax(y_test, axis=1)
    ypred = np.argmax(yhat, axis=1)

    print(multilabel_confusion_matrix(ytrue, ypred))
    print("Accuracy:", accuracy_score(ytrue, ypred))
