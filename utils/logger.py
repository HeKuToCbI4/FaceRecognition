from datetime import datetime


### TODO: possibly add features to log at same file from different loggers. (Simplify log analysis)
class Logger:
    """
    Class for logging strings and writing logfile.
    """

    def __init__(self, logger_name: str, *, log_to_file: bool = False, log_file_name: str = None):
        """
        Initialize Logger
        :param logger_name: Logger name which will be used in output
        :param log_to_file: False by default, determines if logger output should be saved in a file
        :param log_file_name: log file name to write into, by default it is set to LoggerName.txt
        """
        self._logger_name = logger_name
        self._log_to_file = log_to_file
        if log_to_file:
            self._log_file = open(log_file_name if log_file_name is not None else logger_name + '.txt', 'w+')

    def log_string(self, log_string: str):
        """
        method used to log any info in format of 'LoggerName Datetime log_string'
        if log_to_file set to True also writes same string into log file.
        :param log_string: string to log
        :return: None by default
        """
        time = datetime.now()
        string_to_log = f'{self._logger_name} {time.strftime("%H:%M:%S.%f")} {log_string}'
        print(string_to_log)
        if self._log_to_file:
            self._log_file.write(string_to_log)
