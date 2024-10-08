import logging
import confuse
from threading import RLock
from analytics.configs import (
    LOG_CONFIG_TEMPLATE,
    GPM_CLIENT_CONFIG_TEMPLATE,
    ADC_CONFIG_TEMPLATE,
    METRICS_CONFIG_TEMPLATE,
    PROCESSING_CONFIG_TEMPLATE,
    LoggerConfig,
)

base_config_template = {
    "log": LOG_CONFIG_TEMPLATE,
    "gpm": GPM_CLIENT_CONFIG_TEMPLATE,
    "adc": ADC_CONFIG_TEMPLATE,
    "metrics": METRICS_CONFIG_TEMPLATE,
    "processing": PROCESSING_CONFIG_TEMPLATE,
}

config = confuse.LazyConfig(__name__, __name__)
logging = logging.getLogger(__name__)

_config_initialized = False
_init_lock = RLock()

ANALYTICS_ASCII = R"""
    ___                __      __  _          
   /   |  ____  ____ _/ /_  __/ /_(_)_________
  / /| | / __ \/ __ `/ / / / / __/ / ___/ ___/
 / ___ |/ / / / /_/ / / /_/ / /_/ / /__(__  ) 
/_/  |_/_/ /_/\__,_/_/\__, /\__/_/\___/____/  
                     /____/                 
"""
NEW_LINE = "\n"
BYLINE = "Developed at UBC Bionics (http://www.ubcbionics.com)"
VERSION_LINE = "Signal processing module for Grasp | Version 0.0.1"


def _print_module_info():
    print(ANALYTICS_ASCII)
    print(VERSION_LINE)
    print(BYLINE)
    print(NEW_LINE)


def initialize_config_and_logging():
    with _init_lock:
        global _config_initialized
        if not _config_initialized:
            # Read environment variable overrides in to config
            config.set_env()
            # Validate that config conforms to template
            config.get(base_config_template)
            LoggerConfig.configure_logging(config["log"])
            _config_initialized = True
            _print_module_info()
