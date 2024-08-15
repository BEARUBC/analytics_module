import confuse

### This file defines config options for the `metrics` module

METRICS_CONFIG_TEMPLATE = {
    "port": confuse.Optional(int, 9998)
}
