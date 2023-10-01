import pandas as pd
import numpy as np
from numpy import loadtxt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/../../data/Data"
data = []


def get_user_ids():
    return [f.name for f in os.scandir(data_path) if f.is_dir()]


def get_labeled_ids():
    lines = loadtxt(f"{dir_path}/../../data/labeled_ids.txt", dtype=str)

    return lines


def get_activities_df(user_id):
    for _, _, files in os.walk(f"{data_path}/{user_id}/Trajectory"):
        activities = pd.DataFrame(
            columns=["id"], data={"id": [name.split(".")[0] for name in files]}
        )
        activities["user_id"] = user_id

        if user_id in get_labeled_ids():
            activities[
                ["transportation_mode", "start_date_time", "end_date_time"]
            ] = loadtxt(
                f"{data_path}/{user_id}/labels.txt",
                skiprows=1,
                delimiter="\t",
                dtype=str,
            )
        else:
            activities["transportation_mode"] = float("nan")
            activities["start_date_time"] = float("nan")
            activities["end_date_time"] = float("nan")

        return activities


def get_trajectories_df(user_id, activity_id):
    for _, _, files in os.walk(f"{data_path}/{user_id}/Trajectory"):
        trajectories = pd.DataFrame()
        for name in files:
            # if activity_id == name.split(".")[0]:
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
            trajectory["activity_id"] = name.split(".")[0]

            # Add trajectory to trajectories dataframe
            trajectories = pd.concat([trajectories, trajectory])

        return trajectories


def load_data():
    """Load data from the dataset"""
