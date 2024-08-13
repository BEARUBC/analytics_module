import confuse

### This file contains source to parse metrics server configs

METRICS_CONFIG_TEMPLATE = {
    "port": confuse.Optional(int, 9998)
}
