#!/bin/python3
from prometheus_client import start_http_server, Summary
import random
import time
import os
import yaml
from prometheus_client.core import GaugeMetricFamily, REGISTRY


paths=[]
with open("config/paths.yaml", 'r') as stream:
    data = yaml.safe_load(stream)
    paths=data['paths']


def get_dir_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size#in bytes


class CustomCollector(object):    
    def collect(self):
        g = GaugeMetricFamily("file_size", 'File Size',labels=["path"])
        for path in paths:
            path_folder_name = path
            g.add_metric([path_folder_name],get_dir_size(start_path=path))
        yield g

REGISTRY.register(CustomCollector())



# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
TIME_GAP = 10 #seconds

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    port = 8000
    start_http_server(port)
    print(f"Prometheus File Size Stat exporter started on http://localhost:{port}")
    # Generate some requests.
    while True:
        # get_size()
        # time.sleep(TIME_GAP)
        process_request(random.random())