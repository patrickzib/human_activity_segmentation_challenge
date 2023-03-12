import numpy as np
import pandas as pd


def load_data(data_path="../datasets/has_challenge_no_labels.csv.zip"):
    """
    Load the given CSV file containing the sensor data for the challenge.
    Returns a pandas DataFrame where each column is a sensor measurement and
    each row corresponds to a single time series of sensor data.

    Parameters
    ----------
    data_path : str, default: "../datasets/has_challenge_no_labels.csv.zip".
        Path to the csv file to be loaded.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the sensor data for the challenge.

    Examples
    --------
    >>> data = load_data()
    >>> data.head()
    """
    np_cols = ["x-acc", "y-acc", "z-acc",
               "x-gyro", "y-gyro", "z-gyro",
               "x-mag", "y-mag", "z-mag",
               "lat", "lon", "speed"]
    converters = {
        col: lambda val: np.array([]) if len(val) == 0 else np.array(eval(val)) for col
        in np_cols}
    return pd.read_csv(data_path, converters=converters, compression="zip")


def to_submission(df, change_points):
    """
    Convert the change points predicted by an algorithm into the format required for
    submission.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the 250 time series data to be segmented.
    change_points : dict
        A list containing the change points as numpy arrays for each time series
        of the in the DataFrame.

    Returns
    -------
    pandas.DataFrame
        DataFrame with two columns: 'Id' and 'Offsets'. The 'Id' column should contain
        the row indices of the original DataFrame, and the 'Offsets' column contain
        CPs and segment lengths as a string in the format
        '<change point> <segment length>'.
    """
    prediction = []

    for ID, row in df.iterrows():
        ts_len = row["x-acc"].shape[0]   # length of the time series
        segments = np.concatenate(([1], np.sort(change_points[ID]) + 1, [ts_len]))

        for idx in range(segments.shape[0] - 1):
            cp = segments[idx]
            seg_len = segments[idx + 1] - segments[idx]

            prediction.append((ID, f"{int(cp)} {int(seg_len)}"))

    return pd.DataFrame.from_records(prediction, columns=["Id", "Offsets"])
