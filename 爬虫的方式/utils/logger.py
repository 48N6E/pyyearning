from loguru import logger as loguru_logger
import sys

# echo 颜色表
# 红色
_error = "\033[31m %s \033[0m"
# 绿色
_success = "\033[32m %s \033[0m"
# 黄色
_warn = "\033[33m %s \033[0m"
# 蓝色
_cmd = "\033[34m %s \033[0m"
# 白色
_message = "\033[37m %s \033[0m"

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{message}"},
    ]
}
loguru_logger.configure(**config)


class Logger:

    @staticmethod
    def error(message):
        loguru_logger.info(_error % ('[✘] ' + message))

    @staticmethod
    def warn(message):
        loguru_logger.info(_warn % ('[警告] ' + message))

    @staticmethod
    def info(message):
        loguru_logger.info(message)

    @staticmethod
    def success(message):
        loguru_logger.info(_success % ('[✔] ' + message))

    @staticmethod
    def cmd(message):
        loguru_logger.info(_cmd % ('> ' + message))

    @staticmethod
    def flow(title, message=''):
        title = '[%s] ' % title
        loguru_logger.info(_cmd % (title + message))

    @staticmethod
    def message(message):
        # loguru_logger.info(_message % message)
        loguru_logger.info(message)

    @staticmethod
    def logs(message):
        loguru_logger.info(_success % ("     %s " % message))


logger = Logger

