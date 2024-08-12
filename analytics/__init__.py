import logging
import confuse
from threading import RLock
from analytics.common.logging import LOG_CONFIG_TEMPLATE, LoggerConfig

base_config_template = {
    "log": LOG_CONFIG_TEMPLATE,
    "printConfigOnly": bool,
}

config = confuse.LazyConfig(__name__, __name__)
logging = logging.getLogger(__name__)

_config_initialized = False
_initialized = False
_init_lock = RLock()

def initialize_config_and_logging():
    with _init_lock:
        global _config_initialized
        if not _config_initialized: 
            # Read environment variable overrides in to config
            config.set_env()
            # Validate that config conforms to template
            config.get(base_config_template)
            LoggerConfig.configure_logging(config["log"], print_log_config_to_stdout=True)
            _config_initialized = True
