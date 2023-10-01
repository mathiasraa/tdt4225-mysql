import pandas as pd
import numpy as np
from numpy import loadtxt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/../../data/Data"
data = []


def get_user_ids():
    """Returns a list of the user ids

    Returns:
        list[str]
    """

    return [f.name for f in os.scandir(data_path) if f.is_dir()]


def get_labeled_ids():
    """Returns a list of the user ids that have labeled activities

    Returns:
        list[str]
    """

    lines = loadtxt(f"{dir_path}/../../data/labeled_ids.txt", dtype=str)

    return list(lines)


def get_activities_df(user_id: str):
    """Returns a DataFrame of the activities of a user_id

    Arguments:
        user_id {string} -- The id of the user

    Returns:
        DataFrame
    """

    # Create an empty DataFrame to store the activities
    activities = pd.DataFrame(
        columns=[
            "start_date_time",
            "end_date_time",
            "transportation_mode",
            "user_id",
            "id",
        ]
    )

    # Check if the user has labeled activities
    if user_id in get_labeled_ids():
        # Read the labels.txt file into a DataFrame
        activities[
            ["start_date_time", "end_date_time", "transportation_mode"]
        ] = loadtxt(
            f"{data_path}/{user_id}/labels.txt",
            skiprows=1,
            delimiter="\t",
            dtype=str,
        )

        # Clean columns
        activities["user_id"] = user_id
        activities["start_date_time"] = pd.to_datetime(
            activities["start_date_time"], format="%Y/%m/%d %H:%M:%S"
        )
        activities["end_date_time"] = pd.to_datetime(
            activities["end_date_time"], format="%Y/%m/%d %H:%M:%S"
        )
        activities["id"] = (
            activities["start_date_time"]
            .astype(str)
            .str.replace("-", "")
            .str.replace(" ", "")
            .str.replace(":", "")
        )

        return activities


def get_trajectories_df(user_id: str):
    """Returns a DataFrame of the trajectories of a user_id

    Arguments:
        user_id {string} -- The id of the user

    Returns:
        DataFrame
    """

    for _, _, files in os.walk(f"{data_path}/{user_id}/Trajectory"):
        # Create an empty DataFrame to store the trajectories
        trajectories = pd.DataFrame(
            columns=["latitude", "longitude", "altitude", "date_time", "activity_id"]
        )
        activities = get_activities_df(user_id)

        # Check if the user has labeled activities
        if activities.empty:
            return trajectories

        # Loop through the files in the Trajectory folder
        for name in files:
            trajectory = pd.read_csv(
                f"{data_path}/{user_id}/Trajectory/{name}",
                names=[
                    "latitude",
                    "longitude",
                    "_",
                    "altitude",
                    "days",
                    "date",
                    "time",
                ],
                sep=",",
                encoding="ISO-8859-1",
                skiprows=6,
            )
            trajectory["date_time"] = pd.to_datetime(
                trajectory["date"] + " " + trajectory["time"],
                format="%Y-%m-%d %H:%M:%S",
            )
            trajectory = trajectory.drop(columns=["_", "date", "time", "days"])

            # Add trajectory to trajectories dataframe
            trajectories = pd.concat([trajectories, trajectory])

        # Create an empty list to store selected trajectories
        selected_trajectories = []

        # Loop through activities and filter trajectories
        for _, activity in activities.iterrows():
            mask = (trajectories["date_time"] >= activity["start_date_time"]) & (
                trajectories["date_time"] <= activity["end_date_time"]
            )
            trajectory = trajectories.copy()[mask]

            if not trajectory.empty:
                trajectory["activity_id"] = activity["id"]
                selected_trajectories.append(trajectory)

        # Concatenate the selected trajectories into a single DataFrame
        trajectories = pd.concat(selected_trajectories)
        trajectories = trajectories.reset_index(drop=True)

        return trajectories
