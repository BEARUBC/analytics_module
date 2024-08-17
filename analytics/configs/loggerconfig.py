import json
import confuse
from logging.config import dictConfig

### This file defines config options for application-wide `logger`

_log_handler_template = {
    "class": str,
    "level": confuse.Optional(str, None),
    "formatter": confuse.Optional(str, None),
    "filters": confuse.Optional(confuse.StrSeq(), None)
}

_log_logger_template = {
    "level": confuse.Optional(
        confuse.OneOf(
            [
                "TRACE",
                "DEBUG",
                "INFO",
                "WARNING",
                "WARN",
                "ERROR",
                "CRTICAL",
                "FATAL",
                "NOTSET"
            ]
        ),
        None,
    ),
    "propagate": confuse.Optional(bool, None),
    "filters": confuse.Optional(confuse.StrSeq(), None),
    "handlers": confuse.Optional(confuse.StrSeq(), None),
}

LOG_CONFIG_TEMPLATE = {
    "formatters": confuse.Optional(confuse.MappingValues(dict), {}),
    "filters": confuse.Optional(confuse.MappingValues(dict), {}),
    "handlers": confuse.Optional(confuse.MappingValues(dict), {}),
    "loggers": confuse.Optional(confuse.MappingValues(_log_logger_template), {}),
    "root": confuse.Optional(_log_handler_template, {}),
    "incremental": confuse.Optional(bool, {}),
    "disable_existing_loggers": confuse.Optional(bool, {}),
}

class LoggerConfig:
    @classmethod
    def configure_logging(cls, config: confuse.ConfigView, print_log_config_to_stdout: bool = False) -> None:
        """
        Set global config based on the given config object. This serves as a thin wrapper around the
        standard `logging.config.dictConfig` method.

        :param config: ConfigView corresponding to the LOG_CONFIG_TEMPLATE
        :param print_log_config_to_stdout: Flag indicating whether we should print the logger config to stdout
        """
        config_dict = config.get(LOG_CONFIG_TEMPLATE)
        if print_log_config_to_stdout:
            print(f'Initializing logging with config={json.dumps(config_dict | {"version": 1})}')
        dictConfig(config_dict | {"version": 1})
