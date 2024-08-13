import confuse

### This file contains source to parse GPM client configs

GPM_CLIENT_CONFIG_TEMPLATE = {
    "host": confuse.Optional(str, "127.0.0.1"),
    "port": confuse.Optional(int, 4760),
    "read_buffer_size": confuse.Optional(int, 1024)
}
