from analytics.metrics.constants import METRICS_HTTP_PORT
from prometheus_client import start_http_server

def start_metrics_server():
    start_http_server(METRICS_HTTP_PORT)