import os

# 项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志目录
_log_dir = os.path.join(base_dir, 'logs')
if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)

# 日志配置
logging_dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[[%(levelname)-7s] %(asctime)s '
                      'file: %(pathname)s, func: %(funcName)s, '
                      'line: %(lineno)d, msg: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(base_dir, 'logs/access.log'),
            'maxBytes': 1024 * 1024 * 1024,  # 500M
            'backupCount': 10
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'default'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
