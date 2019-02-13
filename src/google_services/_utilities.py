"""Collection of function enabling easier code writing for other packages

"""

from functools import wraps
import pickle
import logging

FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d'
logging.basicConfig(format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger('default')
logger.setLevel(logging.INFO)


# https://stackoverflow.com/questions/4669391/
# python-anyone-have-a-memoizing-decorator-that-can-handle-unhashable-arguments
def memoize(f: callable)->callable:
    """Memoization decorator

    Enables to activate caching on a function: calling it with arguments it
    has already been called with will just return the results from the first
    call, without actually re-running the function.

    Caching is done with regard to the recursive dump of the representation
    of the arguments in memory: any change to in-memory components of the
    arguments will be detected. Changes to remote (ex: on cloud) or hard-drive
    files will not.

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


def apply_defaults(**default_args_getter)->callable:
    """Use the result of a callable as default argument

    Having this on a function on top of memoization allows for
    lazy instantiation of complex default arguments.

    This is useful to create the google-api services. Indeed, we only know
    which credentials to use at run-time, not at import time.

    Args:
        **default_args_getter (dict of {arg_name: callable} pairs): a dictionary
            specifying a function to call (with no arguments) to get the
            default values for the arguments specified as keys
    Returns:
        decorator
    """
    def decorator(f: callable):
        """Instantiate unspecified kwargs with a callable (decorator)

        Args:
            f (callable): the function to wrap

        Returns:
            helper (callable): the wrapper, behaving as f
        """

        @wraps(f)
        def helper(*args, **kwargs):
            """Instantiate unspecified kwargs with a callable (helper)

            Look for keys (aka arg-names) present in `default_args_getter`
            and not present in `kwargs`. Add them to `kwargs`, with the
            result of the corresponding function in `default_args_getter` as
            value.

            Args:
                *args (iterable): positional arguments passed to the function
                **kwargs (dict): keyword arguments passed to the function

            Returns:
                result of applying f onto `args` and the extended `kwargs`
            """
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
