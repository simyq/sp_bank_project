"""
Module with decorators, unused decorator open_file_safely may be useful for working with opening files
"""

from functools import wraps

# from pathlib import Path
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Decorator function for logging the name of the function, its result and Exceptions if any have been called.
    :param filename: name of the file for writing the result. If not given, outputs the result directly to the console
    :return: Decorated function
    """

    def write_log(message: str) -> None:
        """
        Inner function for writing the message to the console or file.
        :return: None
        """

        if filename:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        else:
            print(message)

    def outer_wrapper(func: Callable) -> Callable:

        @wraps(func)
        def inner_wrapper(*args: Any, **kwargs: Any) -> Any:
            function_name = func.__name__

            try:
                result = func(*args, **kwargs)
                success_message = f"{function_name} successfully logged."
                write_log(success_message)
                return result

            except Exception as e:
                error_message = (
                    f"{function_name} failed to log. {type(e).__name__}: {str(e)}. inputs: {args}; {kwargs}"
                )
                write_log(error_message)
                raise

        return inner_wrapper

    return outer_wrapper


# def open_file_safely(func: Callable) -> Callable:
#     """
#     Decorator function. Checks if path to file and file are valid to read
#     (if path is not given, if file is not found, is broken (or is not file), or is empty).
#     :param func: function, which takes path as an argument
#     :return: wrapper: result of inner function execution or an empty list
#     """
#
#     @wraps(func)
#     def wrapper(filename: Optional[str] = None) -> Any:
#         """
#         Inner function for execution of the decorated function.
#         :param filename: str - path of the file to check
#         :return: Any type of the executed function result or an empty list
#         """
#
#         res = []
#
#         if filename:
#             path = Path(filename)
#
#             if path.exists() and path.is_file() and path.stat().st_size > 0:
#                 res = func(filename)
#
#         return res
#
#     return wrapper
