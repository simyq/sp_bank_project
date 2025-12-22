""" Module for relieving working with directories """

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

PATHS = {'src': PROJECT_ROOT / 'src',
         'tests': PROJECT_ROOT / 'tests',
         'logs':PROJECT_ROOT / 'logs',
         'data': PROJECT_ROOT / 'data'}


def get_log_path(filename: str) -> Path:
    """
    Takes a filename and returns the full path of the log file
    :param filename: string name of the file, if the directory does not exist, creates one
    :return: Path of the log file
    """

    log_dir = PATHS['logs']
    log_dir.mkdir(exist_ok=True)

    return log_dir / filename


def get_data_path(filename: str) -> Path:
    """
    Takes a filename and returns the full path of the data file
    :param filename: string name of the file, if the directory does not exist, creates one
    :return: Path of the data file
    """

    data_path = PATHS['data']
    data_path.mkdir(exist_ok=True)
    return data_path / filename


def get_tests_path(filename: str) -> Path:
    """
    Takes a filename and returns the full path of the tests file
    :param filename: string name of the file
    :return: path of the tests file
    """

    tests_path = PATHS['tests']
    return tests_path / filename


def get_src_path(filename: str) -> Path:
    """
    Takes a filename and returns the full path of the src file
    :param filename: string name of the file
    :return: path of the src file
    """

    src_path = PATHS['src']
    return src_path / filename
