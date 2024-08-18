import logging
from prometheus_client import start_http_server
from analytics import config

### This file contains the Prometheus exporter server and our metric definitions

logger = logging.getLogger(__name__)


def start_metrics_server():
    METRICS_PORT = config["metrics"]["port"].as_number()
    start_http_server(METRICS_PORT)
    logger.info(f"Metrics server listening on 0.0.0.0:{METRICS_PORT}")
