import logging
import time

from .exceptions import Example

logger = logging.getLogger("ingredients.utils")

TASK_NOT_FOUND_RETRY_CONFIG = {
    "times": 1,
    "incremental_wait": 0.1,
    "on_exceptions": (Example,),
}


def retry(times, incremental_wait, on_exceptions):
    """retry decorator:
    - Retries the given func if any of {on_exceptions} happens
    - It will retry the execution until {times} times, so, in the worse case,
        it will run the func {times+1} times.
    - Every time that retry the execution will wait an incremental of
        {incremental_wait}. I.E: incremental_wait = 0.3sec, so it will wait 0.3s
        in the first time, 0.6s in the second, 0.9s in the third and goes on...
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            return execute_recursively(1, *args, **kwargs)

        def execute_recursively(count, *args, **kwargs):
            try:
                return function(*args, **kwargs)
            except on_exceptions:
                if count <= times:
                    logger.warning(
                        "Retrying failed function\n"
                        f"Function: {function.__name__}\n"
                        f"Counter: {count} out of {times}",
                        exc_info=True,
                    )
                    time.sleep(incremental_wait * count)
                    return execute_recursively(count + 1, *args, **kwargs)
                else:
                    raise
            else:
                logger.debug(f"Function: {function.__name__} succeeded")

        return wrapper

    return decorator
