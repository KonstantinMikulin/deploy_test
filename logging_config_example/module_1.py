import logging

from module_2 import devide_number
from module_3 import square_number

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'ERROR'


formatter_1 = logging.Formatter(
    fmt='[%(asctime)s] #%(levelname)-8s %(filename)s:'
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

error_file = logging.FileHandler('error.log', 'w', encoding='utf-8')
error_file.setLevel(logging.DEBUG)

error_file.addFilter(ErrorLogFilter())

error_file.setFormatter(formatter_1)

logger.addHandler(error_file)


def main():
    a, b = 12, 2
    c, d = 4, 0

    logger.debug('Лог DEBUG')
    logger.info('Лог INFO')
    logger.warning('Лог WARNING')
    logger.error('Лог ERROR')
    logger.critical('Лог CRITICAL')

    print(devide_number(a, square_number(b)))
    print(devide_number(c, square_number(d)))
