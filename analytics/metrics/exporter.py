from analytics.metrics.constants import METRICS_HTTP_PORT
from prometheus_client import start_http_server

### This file contains the Prometheus exporter server and our metric definitions

def start_metrics_server():
    start_http_server(METRICS_HTTP_PORT)