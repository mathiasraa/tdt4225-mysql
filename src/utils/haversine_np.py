import numpy as np


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points using haversine function.
    Vectorized version of the haversine distance for numpy arrays.

    Fetched from https://stackoverflow.com/a/29546836
    """

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6378.137 * c

    return km
