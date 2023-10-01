# %%
import pandas as pd
import numpy as np
import os


# %%
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "/../../data/Data"
data = []

# for root, dirs, files in os.walk(data_path, topdown=False):
#     for name in dirs:
#         print(name)

print([f.name for f in os.scandir(data_path) if f.is_dir()])

# %%


for f in os.scandir(data_path):
    if f.is_dir():
        for root, dirs, files in os.walk(f"{f.path}/Trajectory"):
            trajectories = []
            for name in files[0]:
                trajectories.append(
                    np.genfromtxt(
                        f"{f.path}/Trajectory/{name}", delimiter=",", skip_header=6
                    )
                )
            data.append(trajectories)

print(data[0])

# %%


def load_data():
    """Load data from the dataset"""
