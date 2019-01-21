from functools import wraps
import pickle
import logging

FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d'
logging.basicConfig(format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger('default')
logger.setLevel(logging.INFO)


# https://stackoverflow.com/questions/4669391/
# python-anyone-have-a-memoizing-decorator-that-can-handle-unhashable-arguments
def memoize(f):
    """Memoization decorator
    Args:
        f (callable): the function that should use memoization
    Returns:
        callable: a version of f using memoization
    """
    memo = {}

    @wraps(f)
    def helper(*args, **kwargs):
        key = pickle.dumps(args, 1) + pickle.dumps(kwargs, 1)
        if key not in memo.keys():
            memo[key] = f(*args, **kwargs)

        return memo[key]
    return helper


def apply_defaults(**default_args_getter):
    """Decorator to use the result of a callable as default argument

    Having memoization on the default_args_getter using memoization allows for
    lazy instantiation of complex default arguments.

    This allows to avoid defining the google api services at import time,
    which could cause the script to crash.

    Args:
        **default_args_getter (dict of (arg, callable) pairs): a dictionary
            specifying a function to call (with no arguments) to get the
            default values for the arguments specified as keys
    Returns:
        decorator
    """
    def decorator(f):

        @wraps(f)
        def helper(*args, **kwargs):
            kwargs = {
                **kwargs,
                **{arg: default_args_getter[arg]()
                   for arg in default_args_getter.keys()
                   if arg not in kwargs.keys()
                   or kwargs[arg] is None}
            }
            return f(*args, **kwargs)
        return helper
    return decorator
