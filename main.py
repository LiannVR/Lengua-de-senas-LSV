from gui.app import run_app
from data.collector import collect_data
from model.train import train_model
from realtime.inference import realtime_test


if __name__ == "__main__":
    run_app()
