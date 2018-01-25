from __future__ import division
import os
import datetime as dt
import random


def save_data(df, filename, sep='|', subdir='data'):
    """Saves a Pandas data frame to the a directory within the project.

    Args:
        df (pd.DataFrame): Source data frame.
        filename (str): Target file name.
        sep (str): Column-delimiter to use.

    """
    tdir = os.path.join(os.getcwd(), os.pardir, subdir, filename)
    df.to_csv(path_or_buf=tdir, sep=sep, header=True, index=False)


def get_datafile(filename):
    """Gets absolute path for any file in the 'data' directory.

    Args:
        filename (str): Name of input file.
    Returns:
        filepath (str): Full absolute path of input file name.

    """
    p = os.path.abspath(os.path.join(os.curdir, os.pardir))
    filepath = os.path.join(p, 'data', filename)

    return filepath


def daterange(start_date, end_date, offset=1):
    """Date range iterator.

    Args:
        start_date (datetime.datetime): Starting date for range.
        end_date (datetime.datetime): Ending date for range.
        offset (int): Step size for iterator (number of days).
    Yields:
        datetime.datetime: The next date in the integer range between
        start_date and end_date, with offset as step size.

    """
    for n in range(0, int((end_date - start_date).days), offset):
        yield start_date + dt.timedelta(n)


def random_date(start=dt.datetime(1900, 1, 1), end=dt.datetime(2017, 12, 31)):
    """Returns a randomly generated date as a datetime object between a range
    of datetime objects.

    Args:
        start (datetime.datetime): Start of date range.
        end (datetime.datetime): End of date range.
    Returns:
        Randomly generated datetime object.

    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    rand_second = random.randrange(int_delta)
    return start + dt.timedelta(seconds=rand_second)
