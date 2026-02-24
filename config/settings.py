import os
import numpy as np

# ==========================
# Paths
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, 'MP_DATA')
LOGS_PATH = os.path.join(BASE_DIR, 'Logs')
MODEL_PATH = os.path.join(BASE_DIR, 'action.h5')

# ==========================
# Dataset
# ==========================

NO_SEQUENCES = 150
SEQUENCE_LENGTH = 30

# 33 pose * 4 + 468 face * 3 + 21 lh * 3 + 21 rh * 3
KEYPOINTS_DIM = 1662

# ==========================
# Training
# ==========================
EPOCHS = 50
TEST_SIZE = 0.20

# ==========================
# Realtime inference
# ==========================
THRESHOLD = 0.7

# ==========================
# Security
# ==========================
ADVANCED_PASSWORD = "admin123"  # cámbiala cuando quieras
