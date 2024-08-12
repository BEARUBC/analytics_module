import logging 
from analytics.metrics.constants import METRICS_HTTP_PORT
from prometheus_client import start_http_server

### This file contains the Prometheus exporter server and our metric definitions

logger = logging.getLogger(__name__)

def start_metrics_server():
    start_http_server(METRICS_HTTP_PORT)
    logger.info(f"Started metrics server at 0.0.0.0:{METRICS_HTTP_PORT}")