import cv2
import numpy as np
import mediapipe as mp

from core.mediapipe_utils import mediapipe_detection, draw_styled_landmarks
from core.keypoints import extract_keypoints
from tensorflow.keras.models import load_model
from config.settings import ACTIONS, MODEL_PATH, THRESHOLD


def realtime_test():
    model = load_model(MODEL_PATH)

    sequence = []
    sentence = []

    cap = cv2.VideoCapture(0)
    mp_holistic = mp.solutions.holistic

    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:

        while cap.isOpened():
            ret, frame = cap.read()
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]

                if res[np.argmax(res)] > THRESHOLD:
                    action = ACTIONS[np.argmax(res)]
                    if len(sentence) == 0 or action != sentence[-1]:
                        sentence.append(action)

                sentence = sentence[-5:]

            cv2.rectangle(image, (0, 0), (640, 40), (0, 0, 0), -1)
            cv2.putText(
                image,
                ' '.join(sentence),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            cv2.imshow("Realtime Test", image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()