import cv2
import numpy as np
import mediapipe as mp
from collections import deque

from core.mediapipe_utils import mediapipe_detection, draw_styled_landmarks
from core.keypoints import extract_keypoints
from tensorflow.keras.models import load_model
from config.settings import (
    MODEL_PATH,
    THRESHOLD,
    SEQUENCE_LENGTH
)
from config.actions import load_actions

ACTIONS = load_actions()

def realtime_test():
    model = load_model(MODEL_PATH)

    sequence = []
    sentence = []
    predictions = []
    prediction_buffer = deque(maxlen=5)

    NOTHING_INDEX = np.where(ACTIONS == "NOTHING_POSE")[0][0]

    cap = cv2.VideoCapture(0)
    mp_holistic = mp.solutions.holistic

    WINDOW_NAME = "Realtime Test"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        while True:

            # 🔴 Cerrar con la X
            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

            ret, frame = cap.read()
            if not ret:
                break

            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-SEQUENCE_LENGTH:]

            if len(sequence) == SEQUENCE_LENGTH:
                res = model.predict(
                    np.expand_dims(sequence, axis=0),
                    verbose=0
                )[0]

                prediction_buffer.append(res)
                avg_res = np.mean(prediction_buffer, axis=0)

                pred_class = np.argmax(avg_res)
                confidence = avg_res[pred_class]

                predictions.append(pred_class)
                predictions = predictions[-5:]

                # 🛑 FILTRO NOTHING_POSE
                if pred_class == NOTHING_INDEX:
                    predictions.clear()
                else:
                    if (
                        confidence > THRESHOLD and
                        predictions.count(pred_class) >= 3
                    ):
                        action = ACTIONS[pred_class]
                        if not sentence or action != sentence[-1]:
                            sentence.append(action)

            sentence = sentence[-5:]
            print(sentence)

            # 🎨 UI
            cv2.rectangle(image, (0, 0), (640, 40), (0, 0, 0), -1)
            cv2.putText(
                image,
                ' '.join(sentence),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            cv2.imshow(WINDOW_NAME, image)

            # ⌨️ Salir con q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
