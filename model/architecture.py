from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from config.settings import (
    SEQUENCE_LENGTH,
    KEYPOINTS_DIM,
)
from config.actions import load_actions

ACTIONS = load_actions()


def build_lstm_model():
    model = Sequential()

    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(SEQUENCE_LENGTH, KEYPOINTS_DIM)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))

    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(len(ACTIONS), activation='softmax'))

    model.compile(
        optimizer='Adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model
