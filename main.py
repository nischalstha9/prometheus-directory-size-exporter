#!/bin/python3
from prometheus_client import start_http_server, Summary
import time
import os
import yaml
import http.server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

config_file_path = "config/paths.yaml"
port = 30000
server_port = 8000

class ServerHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    import urllib
    self.send_response(200)
    self.end_headers()
    if self.path=="/metrics":
        x = urllib.request.urlopen(f'http://0.0.0.0:{port}')
        self.wfile.write(x.read())
    else:
        self.wfile.write(b"Hello World! File Stat Metrics avalilable at: /metrics")


def get_dir_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.stat(fp).st_blocks*512
    return total_size#in bytes


class CustomCollector(object): 
    PATHS=[]

    def __init__(self):
        self.set_paths_from_config()
    
    def set_paths_from_config(self):
        with open(config_file_path, 'r') as stream:
            data = yaml.safe_load(stream)
            try:
                self.PATHS=data['paths']
            except Exception as e:
                print(e)
                pass

    def collect(self):
        g = GaugeMetricFamily("file_size", f'File sizes of given paths in ./{config_file_path}',labels=["path"])
        if len(self.PATHS)>0:
            for path in self.PATHS:
                path_folder_name = path
                g.add_metric([path_folder_name],get_dir_size(start_path=path))
        yield g


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)


if __name__ == '__main__':
    if not os.path.exists(config_file_path):
        while True:
            print(f"Config file not provided at: ./{config_file_path}")
            time.sleep(10)
    else:
        # Start up the server to expose the metrics.
        REGISTRY.register(CustomCollector())
        start_http_server(port)
        server = http.server.HTTPServer(("0.0.0.0", server_port), ServerHandler)
        print(f"Prometheus File Size Stat exporter started on http://localhost:{port}")
        print(f"HTTP server available on port {server_port}")
        print(f"Prometheus metrics available on /metrics")
        server.serve_forever()