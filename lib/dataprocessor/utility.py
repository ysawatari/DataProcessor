# coding=utf-8
"""Utility of dataprocessor.

Some useful tools for dataprocessor are included.

"""
from .exception import DataProcessorError
import os.path


def path_expand(path):
    """Get absolute path.

    Returns
    -------
    str
        Absolute path of the argument

    Raises
    ------
    DataProcessorError
        path is not readable

    """
    if type(path) not in [str, unicode]:
        raise DataProcessorError("path should be str or unicode: %s"
                                 % type(path))
    return os.path.abspath(os.path.expanduser(path))


def check_file(path):
    """Check whether file exists.

    Returns
    -------
    str
        Absolute path of the argument

    Raises
    ------
    DataProcessorError
        occurs in two cases:

        + when the file does not exist
        + file exist but it is a directory

    """
    path = path_expand(path)
    if not os.path.exists(path):
        raise DataProcessorError("File '%s' does not exist" % path)
    if os.path.isdir(path):
        raise DataProcessorError("%s is not a file but a directory" % path)
    return path


def check_directory(path):
    """Check whether file exists.

    Returns
    -------
    str
        Absolute path of the argument

    Raises
    ------
    DataProcessorError
        occurs when the file does not exist or the file is not directory.

    """
    path = path_expand(path)
    if not os.path.exists(path):
        raise DataProcessorError("Directory '%s' does not exist" % path)
    if not os.path.isdir(path):
        raise DataProcessorError("%s is not a directory" % path)
    return path


def get_directory(path, silent=True):
    """Get absolute path of the directory.

    If it does not exist, it will be created.

    Parameters
    ----------
    silent : bool, optional
        does not ask whether create directory (default=True)

    Returns
    -------
    str
        Absolute path of the directory

    Raises
    ------
    DataProcessorError
        occurs in two cases

        + another file (does not directory) exist
        + refused by user to create directory

    """
    dir_path = path_expand(path)
    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise DataProcessorError("Another file already exists in %s"
                                     % dir_path)
        if not silent:
            ans = raw_input("Create directory(%s)? [y/N]" % dir_path)
            if ans not in ["yes", "y"]:
                raise DataProcessorError("Directory cannot be created.")
        os.makedirs(dir_path)
    return dir_path


def boolenize(arg):
    """Make arg boolen value.

    Parameters
    ----------
    arg : bool, str, int, float

    Returns
    -------
    bool

    Examples
    --------
    >>> boolenize(True)
    True
    >>> boolenize(False)
    False

    >>> boolenize(1)
    True
    >>> boolenize(0)
    False
    >>> boolenize(0.0)
    False

    >>> boolenize("True")
    True
    >>> boolenize("other words")
    True
    >>> boolenize("False")
    False
    >>> boolenize("falSE")
    False
    >>> boolenize("false")
    False
    >>> boolenize("F")
    False
    >>> boolenize("f")
    False
    >>> boolenize("No")
    False
    >>> boolenize("NO")
    False
    >>> boolenize("no")
    False
    >>> boolenize("N")
    False
    >>> boolenize("n")
    False

    """
    if type(arg) == str and arg.lower() in ["false", "f", "no", "n"]:
        return False
    return bool(arg)
