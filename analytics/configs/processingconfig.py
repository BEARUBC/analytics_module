import confuse

### This file defines config options for the `processing` module

PROCESSING_CONFIG_TEMPLATE = {
    "sleep_between_processing_in_seconds": confuse.Optional(int, 5)
}
