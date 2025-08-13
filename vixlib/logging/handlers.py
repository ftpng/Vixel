import os
import time
from logging.handlers import TimedRotatingFileHandler

from vixlib import LOGS_DIR
from .formatters import UncoloredFormatter


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        filename='latest.log',
        backup_format='%Y-%m-%d',
        logs_dir=f'{LOGS_DIR}',
        when='d',
        interval=1,
        backupCount=0,
        encoding='utf-8',
        delay=False,
        utc=False,
        atTime=None,
        errors=None,
        formatter=UncoloredFormatter
    ) -> None:
        self.backup_format = backup_format
        self.logs_dir = logs_dir

        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        filename = os.path.join(logs_dir, filename)

        super().__init__(
            filename, when, interval, backupCount,
            encoding, delay, utc, atTime, errors
        )
        self.setFormatter(formatter)


    def rotation_filename(self, default_name) -> str:
        backup_format = time.strftime(self.backup_format)
        backup_format = backup_format.removesuffix('.log')

        base_filename = os.path.splitext(default_name)[0]
        base_filename = os.path.join(self.logs_dir, base_filename + "_" + backup_format)

        i = 1
        suffix = f'_{i}'

        while os.path.exists(f'{base_filename}{suffix}.log'):
            i += 1
            suffix = f'_{i}'

        return f'{base_filename}{suffix}.log'