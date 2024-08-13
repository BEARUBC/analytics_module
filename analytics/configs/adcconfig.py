import confuse

### This file contains source to parse ADC reader configs

ADC_CONFIG_TEMPLATE = {
    "inner_read_buffer_size": confuse.Optional(int, 2000),
    "outer_read_buffer_size": confuse.Optional(int, 2000)
}
