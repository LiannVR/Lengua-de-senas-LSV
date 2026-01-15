import os
import numpy as np

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

from config.settings import (
    DATA_PATH,
    NO_SEQUENCES,
    SEQUENCE_LENGTH
)
from config.actions import load_actions

ACTIONS = load_actions()


def load_sequences():
    """
    Carga los archivos .npy y construye las secuencias y etiquetas
    """
    label_map = {label: num for num, label in enumerate(ACTIONS)}

    sequences = []
    labels = []

    for action in ACTIONS:
        for sequence in range(NO_SEQUENCES):
            window = []

            for frame_num in range(SEQUENCE_LENGTH):
                npy_path = os.path.join(
                    DATA_PATH,
                    action,
                    str(sequence),
                    f"{frame_num}.npy"
                )

                if not os.path.exists(npy_path):
                    raise FileNotFoundError(
                        f"Archivo faltante: {npy_path}"
                    )

                res = np.load(npy_path)
                window.append(res)

            sequences.append(window)
            labels.append(label_map[action])

    X = np.array(sequences)
    y = to_categorical(labels).astype(int)

    return X, y


def get_train_test_data(test_size=0.05, random_state=42):
    """
    Retorna los datos listos para entrenamiento y testeo
    """
    X, y = load_sequences()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    return X_train, X_test, y_train, y_test
