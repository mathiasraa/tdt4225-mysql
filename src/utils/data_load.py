import pandas as pd
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/../../data/Data"
data = []


def get_user_ids():
    return [f.name for f in os.scandir(data_path) if f.is_dir()]


def get_trajectories_df(user_id):
    for _, _, files in os.walk(f"{data_path}/{user_id}/Trajectory"):
        trajectories = pd.DataFrame()
        for name in files:
            trajectory = pd.read_csv(
                f"{data_path}/{user_id}/Trajectory/{name}",
                names=[
                    "latitude",
                    "longitude",
                    ".",
                    "altitude",
                    "days",
                    "date",
                    "time",
                ],
                sep=",",
                encoding="ISO-8859-1",
                skiprows=6,
            )
            trajectory["id"] = name.split(".")[0]

            # Add trajectory to trajectories dataframe
            trajectories = pd.concat([trajectories, trajectory])

        return trajectories


def load_data():
    """Load data from the dataset"""
