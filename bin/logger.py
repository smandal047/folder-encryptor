import os
import logging


# Setting up the logging configuration
log_file = r'logs\cryptor.log'
try:
    with open(log_file, 'r+') as f:
        f.truncate(0) # need '0' when using r+
except FileNotFoundError:
    os.mkdir(os.path.dirname(log_file))


class SingletonLogger:

    _instance = None

    @staticmethod
    def get_instance(log_file="app.log", log_level=logging.DEBUG):
        """
        Static method to retrieve the singleton instance of the logger.
        
        Parameters:
        - log_file (str): The name of the log file. Defaults to 'app.log'.
        - log_level (int): The logging level. Defaults to logging.DEBUG.
        
        Returns:
        - logger (logging.Logger): Configured logger.
        """
        if SingletonLogger._instance is None:
            SingletonLogger._instance = SingletonLogger(log_file, log_level)
        return SingletonLogger._instance.logger

    def __init__(self, log_file="app.log", log_level=logging.DEBUG):
        if SingletonLogger._instance is not None:
            raise Exception("Logger instance already created. Use get_instance() to get the singleton logger.")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create a formatter for log messages
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Log all levels to the file
        file_handler.setFormatter(formatter)

        # Create a stream handler for logging to the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)  # Display only INFO and above in the console
        stream_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
# Usage of SingletonLogger
def logger(log_file=log_file, log_level=logging.DEBUG):
    return SingletonLogger.get_instance(log_file, log_level)