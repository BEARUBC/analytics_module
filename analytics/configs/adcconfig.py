import confuse

### This file defines config options for the `adc` module

ADC_CONFIG_TEMPLATE = {
    "inner_read_buffer_size": confuse.Optional(int, 2000),
    "outer_read_buffer_size": confuse.Optional(int, 2000),
    "mock_reader_state_buffer_size": confuse.Optional(int, 100),
    "sleep_between_reads_in_seconds": confuse.Optional(int, 0.1),
    "use_mock_adc": confuse.Optional(bool, False)
}
