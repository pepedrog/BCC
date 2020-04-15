from functools import wraps

# Final version disables type checking and removes checking overhead.
IS_FINAL_VERSION = False

# Definitions
def __precheck_types(func_annotations, *args, **kwargs):
    annotations = dict((argument, value_type)
                       for argument, value_type in func_annotations.items()
                       if argument != 'return')
    for arg, value in kwargs.items():
        if arg not in annotations:
            continue
        if not isinstance(value, annotations[arg]):
            raise TypeError(f'value \'{value}\' is not of '
                            + f'type {annotations[arg]}')
        del annotations[arg]

    for expected_type, value in zip(annotations.values(), args):
        if not isinstance(value, expected_type):
            raise TypeError(f'value \'{value}\' is not of '
                            + f'type {expected_type}')

def type_checked(bound: bool = False):
    ''' Adds type checking into a function. '''
    def decorator(func):
        if IS_FINAL_VERSION:
            return func
        has_return_type = 'return' in func.__annotations__
        return_type = func.__annotations__.get('return', None.__class__)
        if bound:
            @wraps(func)
            def func_wrapper(self, *args, **kwargs):
                __precheck_types(func.__annotations__, *args, **kwargs)
                result = func(self, *args, **kwargs)
                if has_return_type:
                    if not isinstance(result, return_type):
                        raise TypeError('return type is not of '
                                        + f'type {return_type}')
                return result
        else:
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                __precheck_types(func.__annotations__, *args, **kwargs)
                result = func(*args, **kwargs)
                if has_return_type:
                    if not isinstance(result, return_type):
                        raise TypeError('return type is not of '
                                        + f'type {return_type}')
                return result
        return func_wrapper
    return decorator
