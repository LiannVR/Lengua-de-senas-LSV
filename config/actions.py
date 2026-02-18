import os
import numpy as np
from config.settings import DATA_PATH

def load_actions():
    actions = [
        f for f in os.listdir(DATA_PATH)
        if os.path.isdir(os.path.join(DATA_PATH, f))
    ]
    actions.sort()  # <-- importante: orden consistente
    return np.array(actions)
    

