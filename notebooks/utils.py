import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def load_data(data_path="../datasets/has2023.csv.zip"):
    """
    Load the given CSV file containing the sensor data for the challenge.
    Returns a pandas DataFrame where each column is a sensor measurement and
    each row corresponds to a single time series of sensor data.

    Parameters
    ----------
    data_path : str, default: "../datasets/has2023.csv.zip".
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


def load_master_data(data_path="../datasets/has2023_master.csv.zip"):
    """
    Load the given CSV file containing the labelled challenge data.
    Returns a pandas DataFrame where each column is a sensor measurement
    or label and each row corresponds to a single time series.

    Parameters
    ----------
    data_path : str, default: "../datasets/has2023_master.csv.zip".
        Path to the csv file to be loaded.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the sensor data for the challenge.

    Examples
    --------
    >>> data = load_master_data()
    >>> data.head()
    """
    np_cols = ["change_points", "activities", "x-acc", "y-acc", "z-acc",
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
        DataFrame with two columns: 'ts_id' and 'segment'. The 'Id' column should contain
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

    return pd.DataFrame.from_records(prediction, columns=["ts_id", "segment"])


def visualize_activity_data(title, sensor_names, time_series, change_points, activities, show=True, file_path=None, sample_rate=50,
                       font_size=18):
    """
    Plots multivariate time series data segmented by change points and colored by activity labels.

    Parameters
    ----------
    title : str
        The title of the time series plot.
    sensor_names : list of str
        List of sensor names corresponding to each time series.
    time_series : list of np.ndarray
        List of arrays containing the time series data from sensors.
    change_points : np.ndarray
        Array of change points indicating the indices where activity changes.
    activities : list of str
        List of activity labels corresponding to the segments between change points.
    show : bool, optional
        Whether to display the plot. Default is True.
    file_path : str, optional
        If provided, saves the plot to the given file path.
    sample_rate : int, optional
        Sample rate of the time series data. Default is 50.
    font_size : int, optional
        Font size for the axis labels and title. Default is 18.

    Returns
    -------
    ax : matplotlib.axes._subplots.AxesSubplot
        The last Axes object of the plot.
    """
    plt.clf()
    fig, axes = plt.subplots(
        len(time_series),
        sharex=True,
        gridspec_kw={'hspace': .15},
        figsize=(20, len(time_series) * 2)
    )

    activity_colours = {}
    idx = 0

    for activity in activities:
        if activity not in activity_colours:
            activity_colours[activity] = f"C{idx}"
            idx += 1

    for ts, sensor, ax in zip(time_series, sensor_names, axes):
        if len(ts) > 0:
            segments = [0] + change_points.tolist() + [ts.shape[0]]
            for idx in np.arange(0, len(segments) - 1):
                ax.plot(
                    np.arange(segments[idx], segments[idx + 1]),
                    ts[segments[idx]:segments[idx + 1]],
                    c=activity_colours[activities[idx]]
                )

        ax.set_ylabel(sensor, fontsize=font_size)

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(font_size)

        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(font_size)

    axes[0].set_title(title, fontsize=font_size)
    axes[-1].set_xticklabels([f"{int(tick / sample_rate)}s" for tick in axes[-1].get_xticks()])

    if show is True:
        plt.show()

    if file_path is not None:
        plt.savefig(file_path, bbox_inches="tight")

    return ax