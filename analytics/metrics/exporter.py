from prometheus_client import start_http_server

def start_metrics_server():
    start_http_server(8000)