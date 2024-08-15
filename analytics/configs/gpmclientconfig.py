import confuse

### This file defines config options for the `gpm` module

GPM_CLIENT_CONFIG_TEMPLATE = {
    "host": confuse.Optional(str, "127.0.0.1"),
    "port": confuse.Optional(int, 4760),
    "read_buffer_size": confuse.Optional(int, 1024)
}
