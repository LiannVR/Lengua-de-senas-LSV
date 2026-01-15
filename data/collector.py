import os
import cv2
import numpy as np
import mediapipe as mp

from core.mediapipe_utils import mediapipe_detection, draw_styled_landmarks
from core.keypoints import extract_keypoints
from config.settings import (
    DATA_PATH,
    NO_SEQUENCES,
    SEQUENCE_LENGTH
)
from config.actions import load_actions

ACTIONS = load_actions()

mp_holistic = mp.solutions.holistic

def create_folders_for_action(action):
    """
    Crea la estructura:
    MP_DATA/action/sequence/frame.npy

    - Solo crea carpetas para la acción indicada
    - Continúa la numeración si ya existen datos
    """

    # Crear carpeta base
    os.makedirs(DATA_PATH, exist_ok=True)

    # Ruta de la acción
    action_path = os.path.join(DATA_PATH, action)

    # Crear carpeta de la acción
    os.makedirs(action_path, exist_ok=True)

    # Obtener secuencias existentes (solo carpetas numéricas)
    existing_sequences = [
        int(folder)
        for folder in os.listdir(action_path)
        if folder.isdigit()
    ]

    # Determinar punto de inicio
    start_sequence = max(existing_sequences) + 1 if existing_sequences else 0

    # Crear nuevas secuencias
    for sequence in range(start_sequence, start_sequence + NO_SEQUENCES):
        os.makedirs(
            os.path.join(action_path, str(sequence)),
            exist_ok=True
        )

def collect_data_for_action(action: str, start_sequence: int = 0):
    """
    Recolecta keypoints para entrenamiento y testeo
    SOLO para una acción específica.

    - action: nombre de la acción (ej: "hola")
    - start_sequence: carpeta desde donde iniciar (default 0)
    """

    # Crear carpetas SOLO para esta acción
    create_folders_for_action(action)

    cap = cv2.VideoCapture(0)
    WINDOW_NAME = "OpenCV Feed"

    cv2.namedWindow(WINDOW_NAME)

    with mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        # Recolectar SOLO para la acción indicada
        for sequence in range(start_sequence, start_sequence + NO_SEQUENCES):
            for frame_num in range(SEQUENCE_LENGTH):

                # 🚪 Detectar cierre con X
                if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                ret, frame = cap.read()
                if not ret:
                    continue

                image, results = mediapipe_detection(frame, holistic)
                draw_styled_landmarks(image, results)

                if frame_num == 0:
                    cv2.putText(
                        image,
                        'STARTING COLLECTION',
                        (120, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        4,
                        cv2.LINE_AA
                    )
                    cv2.putText(
                        image,
                        f'Collecting frames for {action} - Video {sequence}',
                        (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA
                    )

                    cv2.imshow(WINDOW_NAME, image)
                    cv2.waitKey(500)
                else:
                    cv2.putText(
                        image,
                        f'Collecting frames for {action} - Video {sequence}',
                        (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA
                    )
                    cv2.imshow(WINDOW_NAME, image)

                keypoints = extract_keypoints(results)

                # ⚠️ Sobrescribe sin problema si ya existe
                np.save(
                    os.path.join(
                        DATA_PATH,
                        action,
                        str(sequence),
                        str(frame_num)
                    ),
                    keypoints
                )

                # Tecla q (opcional)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

    cap.release()
    cv2.destroyAllWindows()

    
def create_folders():
    """
    Crea la estructura:
    MP_DATA/action/sequence/frame.npy
    Continúa la numeración si ya existen datos.
    """

    # Crear carpeta base
    os.makedirs(DATA_PATH, exist_ok=True)

    for action in ACTIONS:
        action_path = os.path.join(DATA_PATH, action)

        # Crear carpeta de la acción
        os.makedirs(action_path, exist_ok=True)

        # Obtener secuencias existentes (solo números)
        existing_sequences = [
            int(folder)
            for folder in os.listdir(action_path)
            if folder.isdigit()
        ]

        # Determinar punto de inicio
        start_sequence = max(existing_sequences) + 1 if existing_sequences else 0

        # Crear nuevas secuencias
        for sequence in range(start_sequence, start_sequence + NO_SEQUENCES):
            os.makedirs(
                os.path.join(action_path, str(sequence)),
                exist_ok=True
            )


    """
    for action in ACTIONS: 
        dirmax = np.max(np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int))
        for sequence in range(1,NO_SEQUENCES+1):
            try: 
                os.makedirs(os.path.join(DATA_PATH, action, str(dirmax+sequence)))
            except:
                pass """
            
    """
    for action in ACTIONS:
        for sequence in range(NO_SEQUENCES):
            os.makedirs(
                os.path.join(DATA_PATH, action, str(sequence)),
                exist_ok=True
            ) """


def collect_data(start_sequence: int = 0):
    """
    Recolecta keypoints para entrenamiento y testeo
    """

    create_folders()

    cap = cv2.VideoCapture(0)
    WINDOW_NAME = "OpenCV Feed"

    cv2.namedWindow(WINDOW_NAME)

    with mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        for action in ACTIONS:
            for sequence in range(start_sequence, start_sequence + NO_SEQUENCES):
                for frame_num in range(SEQUENCE_LENGTH):

                    # 🚪 Detectar cierre con X
                    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                    ret, frame = cap.read()
                    if not ret:
                        continue

                    image, results = mediapipe_detection(frame, holistic)
                    draw_styled_landmarks(image, results)

                    if frame_num == 0:
                        cv2.putText(
                            image,
                            'STARTING COLLECTION',
                            (120, 200),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            4,
                            cv2.LINE_AA
                        )
                        cv2.putText(
                            image,
                            f'Collecting frames for {action} - Video {sequence}',
                            (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            1,
                            cv2.LINE_AA
                        )

                        cv2.imshow(WINDOW_NAME, image)
                        cv2.waitKey(500)
                    else:
                        cv2.putText(
                            image,
                            f'Collecting frames for {action} - Video {sequence}',
                            (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            1,
                            cv2.LINE_AA
                        )
                        cv2.imshow(WINDOW_NAME, image)

                    keypoints = extract_keypoints(results)
                    np.save(
                        os.path.join(DATA_PATH, action, str(sequence), str(frame_num)),
                        keypoints
                    )

                    # Tecla q (opcional mantenerla)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return

    cap.release()
    cv2.destroyAllWindows()


    """ create_folders()

    cap = cv2.VideoCapture(0)

    with mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        # Loop por acción
        for action in ACTIONS:

            # Loop por secuencia (video)
            for sequence in range(start_sequence, start_sequence + NO_SEQUENCES):

                # Loop por frames
                for frame_num in range(SEQUENCE_LENGTH):

                    ret, frame = cap.read()
                    if not ret:
                        continue

                    # Detección MediaPipe
                    image, results = mediapipe_detection(frame, holistic)
                    draw_styled_landmarks(image, results)

                    # Mensajes en pantalla
                    if frame_num == 0:
                        cv2.putText(
                            image,
                            'STARTING COLLECTION',
                            (120, 200),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            4,
                            cv2.LINE_AA
                        )
                        cv2.putText(
                            image,
                            f'Collecting frames for {action} - Video {sequence}',
                            (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            1,
                            cv2.LINE_AA
                        )
                        cv2.imshow('OpenCV Feed', image)
                        cv2.waitKey(500)
                    else:
                        cv2.putText(
                            image,
                            f'Collecting frames for {action} - Video {sequence}',
                            (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 0, 255),
                            1,
                            cv2.LINE_AA
                        )
                        cv2.imshow('OpenCV Feed', image)

                    # Extraer y guardar keypoints
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(
                        DATA_PATH,
                        action,
                        str(sequence),
                        str(frame_num)
                    )
                    np.save(npy_path, keypoints)

                    # Salida segura
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return

    cap.release()
    cv2.destroyAllWindows()
 """