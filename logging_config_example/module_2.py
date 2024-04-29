import logging
import sys

logger = logging.getLogger(__name__)


class DebugWarningLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('DEBUG', 'WARNING')


formatter_2 = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(filename)s: '
        '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)

stdout = logging.StreamHandler(sys.stdout)

stdout.addFilter(DebugWarningLogFilter())

stdout.setFormatter(formatter_2)

logger.addHandler(stdout)


def devide_number(divident: int | float, devider: int | float):
    logger.debug('Лог DEBUG')
    logger.info('Лог INFO')
    logger.warning('Лог WARNING')
    logger.error('Лог ERROR')
    logger.critical('Лог CRITICAL')

    try:
        return divident / devider
    except ZeroDivisionError:
        logger.exception('Произошло деление на 0')
