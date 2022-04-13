import time
import requests
import random


class StaticMethod():
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls):
        return self.func


def staticmethod(func):
    return StaticMethod(func)


def measure_time(func):
    """Decorator for printing execution time of the given funcion
    Args:
        func - function to be decorated
    Returns:
        function execution time, float
    """
    def run_func(*args, **kwargs):
        start = time.time()
        try:
            func(*args, **kwargs)
        except TypeError:
            pass
        return time.time() - start
    return run_func


def function_logging(func):
    """Decorator providing logging for input function - input arguments type,
    values, and return type and value are the output of decorated function
    Args:
        func - function to be decorated
    Returns:
        function name, input arguments values and types, function  output
        value and type
    """
    def kwarg_to_string(kwargs):
        return ", ".join(f"{key}={value}" for key, value in kwargs.items())

    def func_logger(*args, **kwargs):
        if len(args) and len(kwargs):
            print(f"Function {func.__name__} is called with "
                  f"positional arguments: {str(args)} "
                  f"and keyword arguments: {kwarg_to_string(kwargs)}")
        elif len(args):
            print(f"Function {func.__name__} is called with positional arguments: {str(args)}")
        elif len(kwargs):
            print(f"Function {func.__name__} is called with keyword arguments: {kwarg_to_string(kwargs)}")
        else:
            print(f"Function {func.__name__} is called with no arguments")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returns output of type {type(result).__name__}")
        return result
    return func_logger


def russian_roulette_decorator(probability, return_value="Ooops, your output has been stolen!"):
    """Decorator replacing function output with message user message
    Args:
        func - function to be decorated
        probability - value between [0, 1] defining chances of the output replacement
        return_value - message to be returned instead of function value
    Returns:
        function output or user message with given probability
    """
    def decorator(func):
        def steal_output(*args, **kwargs):
            if random.uniform(0, 1) < probability:
                return return_value
            else:
                return func(*args, **kwargs)
        return steal_output
    return decorator


if __name__ == "__main__":
    # 1. декоратор, подменивающий возвращаемое значение декорируемой функции на время её выполнения

    @measure_time
    def some_function(a, b, c, d, e=0, f=0, g="3"):
        time.sleep(a)
        time.sleep(b)
        time.sleep(c)
        time.sleep(d)
        time.sleep(e)
        time.sleep(f)
        return g

    print(some_function(1, 2, 3, 4, e=5, f=6, g="99999"))
    # 2. декоратор логгирующий выполнение функции

    @function_logging
    def func1():
        return set()

    @function_logging
    def func2(a, b, c):
        return (a + b) / c

    @function_logging
    def func3(a, b, c, d=4):
        return [a + b * c] * d

    @function_logging
    def func4(a=None, b=None):
        return {a: b}

    print(func1(), end="\n\n")
    print(func2(1, 2, 3), end="\n\n")
    print(func3(1, 2, c=3, d=2), end="\n\n")
    print(func4(a=None, b=float("-inf")), end="\n\n")
    # 3. декоратор, подменяющий значение функции с заданной вероятностью на строку пользователя

    @russian_roulette_decorator(probability=0.2, return_value="Ooops, your output has been stolen!")
    def make_request(url):
        return requests.get(url)

    for _ in range(10):
        print(make_request("https://google.com"))
    # 4. реализация декоратора staticmethod

    class TestClass:
        @staticmethod
        def print_message():
            print('Own staticmethod implemented')

    TestClass.print_message()
