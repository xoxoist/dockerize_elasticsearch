import datetime
import inspect
import logging
import functools
import json
import os.path


class WaveLog:

    def __init__(self, service_name: str, logger_name: str, log_level=logging.INFO):
        self.m_service_name = service_name
        self.m_logger_name = logger_name
        self.m_log_level = log_level
        self.m_logger = logging.getLogger(logger_name)
        frame = inspect.currentframe().f_back
        path = frame.f_globals['__file__']
        self.m_file_name = os.path.basename(path)
        self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        self.m_logger.setLevel(self.m_log_level)

        file_handler = logging.FileHandler(self.m_logger_name + ".log")
        file_handler.setLevel(self.m_log_level)

        self.m_logger.addHandler(file_handler)

    def str_message(self, func_name, param_name: list, args, kwargs):
        argu = ""
        temp_arg: [] = []
        for i, arg in enumerate(args):
            temp_arg.append(f"\"{param_name[i].name}\": \"{args[i]}\", " if i < len(
                args) - 1 else f"\"{param_name[i].name}\": \"{args[i]}\"")
            argu = "".join(temp_arg)

        serialized_kwargs = json.dumps(kwargs).removeprefix('{').removesuffix('}')
        serialzed_args = json.dumps(argu).removeprefix('"').removesuffix('"')

        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        if kwargs == {}:
            return (f"{{\"service\": \"{self.m_service_name}\", \"file\": \"{self.m_file_name}\", "
                    f"\"func\": \"{func_name}\", \"time\": \"{current_timestamp}\", \"msg\": \"\\\"f_args\\\": {{{serialzed_args}}}\"}}")
        if kwargs != {}:
            return (f"{{\"service\": \"{self.m_service_name}\", \"file\": \"{self.m_file_name}\", "
                    f"\"func\": \"{func_name}\", \"time\": \"{current_timestamp}\", \"msg\": \"\\\"f_kwargs\\\": {{{serialized_kwargs}}}}}")

    def logger(self) -> logging.Logger:
        return self.m_logger

    def logit(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signature = inspect.signature(func)
            param_name = list(signature.parameters.values())
            print(kwargs)
            logging.info(f"Executing {func.__name__} with arguments {args} and keyword arguments {kwargs}")
            self.logger().info(
                self.str_message(func_name=func.__name__, param_name=param_name, args=args, kwargs={}))
            if kwargs != {}:
                self.logger().info(
                    self.str_message(func_name=func.__name__, param_name=param_name, args=args,
                                     kwargs=kwargs))
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} execution complete")
            return result

        return wrapper
