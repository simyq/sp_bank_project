"""
Module with decorators
"""

from functools import wraps
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
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        else:
            print(message)

    def outer_wrapper(func: Callable) -> Callable:

        @wraps(func)
        def inner_wrapper(*args: Any, **kwargs: Any) -> Any:
            function_name = func.__name__

            try:
                result = func(*args, **kwargs)
                success_message = f'{function_name} successfully logged.'
                write_log(success_message)
                return result

            except Exception as e:
                error_message = \
                    f'{function_name} failed to log. {type(e).__name__}: {str(e)}. inputs: {args}; {kwargs}'
                write_log(error_message)
                raise

        return inner_wrapper

    return outer_wrapper
