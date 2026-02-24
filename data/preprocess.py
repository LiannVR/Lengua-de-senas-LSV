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


def augment_sequence(sequence, noise_level=0.005):
    """
    Genera una copia aumentada de una secuencia agregando
    ruido gaussiano pequeño a los keypoints.
    Esto ayuda al modelo a generalizar mejor.
    """
    noise = np.random.normal(0, noise_level, sequence.shape)
    return sequence + noise


def load_sequences():
    """
    Carga los archivos .npy y construye las secuencias y etiquetas.
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


def get_train_test_data(test_size=0.05, random_state=42, augment=True):
    """
    Retorna los datos listos para entrenamiento y testeo.
    La augmentation se aplica SOLO sobre los datos de entrenamiento
    para evitar contaminación del test set.
    """
    X, y = load_sequences()

    # Split ANTES de augmentar
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=np.argmax(y, axis=1),  # Distribución balanceada
        random_state=random_state,
    )

    # Augmentar SOLO datos de entrenamiento
    if augment:
        X_aug = np.array([augment_sequence(seq) for seq in X_train])
        X_train = np.concatenate([X_train, X_aug], axis=0)
        y_train = np.concatenate([y_train, y_train], axis=0)

        # Mezclar para que no estén agrupados original/aumentado
        shuffle_idx = np.random.permutation(len(X_train))
        X_train = X_train[shuffle_idx]
        y_train = y_train[shuffle_idx]

        print(f"📈 Data augmentation: {len(X_train)} train + {len(X_test)} test")

    return X_train, X_test, y_train, y_test

