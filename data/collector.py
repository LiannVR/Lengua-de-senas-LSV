import os
import cv2
import numpy as np
import mediapipe as mp

from core.mediapipe_utils import mediapipe_detection, draw_styled_landmarks
from core.keypoints import extract_keypoints
from config.settings import (
    DATA_PATH,
    ACTIONS,
    NO_SEQUENCES,
    SEQUENCE_LENGTH
)


def create_folders():
    """
    Crea la estructura de carpetas:
    MP_DATA/action/sequence/frame.npy
    """
    for action in ACTIONS:
        for sequence in range(NO_SEQUENCES):
            os.makedirs(
                os.path.join(DATA_PATH, action, str(sequence)),
                exist_ok=True
            )


def collect_data(start_sequence: int = 0):
    """
    Recolecta keypoints para entrenamiento y testeo
    """
    create_folders()

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
