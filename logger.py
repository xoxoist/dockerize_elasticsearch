import functools
import logging

# Configure logging to capture messages at the INFO level
logging.basicConfig(level=logging.INFO)


def log_functions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with arguments {args} and keyword arguments {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} execution complete")
        return result

    return wrapper

@log_functions
def test_print(message: str):
    print(message)

@log_functions
def business_logic_function_sample(a: str, b: int, c: float, **kwargs):
    test_print("Hello World")


def main():
    business_logic_function_sample("Hello World", 1090, 29.08, k1="K1", k2=10, k3=True)


if __name__ == "__main__":
    main()
