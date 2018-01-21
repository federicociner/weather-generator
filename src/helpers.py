from __future__ import division, absolute_import
import os


def save_data(df, filename, sep='|'):
    """Saves a Pandas data frame to the data directory within the project.

    Args:
        df (pd.DataFrame): Source data frame.
        filename (str): Target file name.
        sep (str): Column-delimiter to use.

    """
    tdir = os.path.join(os.getcwd(), os.pardir, 'data', filename)
    df.to_csv(path_or_buf=tdir, sep=sep, header=True, index=False)


def get_filepath(filename):
    """ Gets absolute path for any file in the "data" directory.

    Args:
        filename (str): Name of input file.
    Returns:
        filepath (str): Full absolute path of input file name.
    """
    p = os.path.abspath(os.path.join(os.curdir, os.pardir))
    filepath = os.path.join(p, 'data', filename)

    return filepath
