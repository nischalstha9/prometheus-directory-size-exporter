# prometheus-directory-size-exporter

## path.yaml sample

```
paths:
  - "/home/nischal/dev/prometheus-filestat"
  - "/home/nischal/dev/ecommerce"
  - /home/nischal/dev/inventory_management
```

## Run with docker-compose

```
version: "3"
services:
  file_size_exporter:
    build:
      context: .
    ports:
      - 8000:8000
    volumes:
      - ./config:/code/config    #THIS IS CONFIG DIR With path.yaml File...naming convention is strict(THERE MUST BE path.yaml file with paths[])
      - ./protected:/protected
      - /home/nischal/dev/inventory_management:/inventory_mgmt_fronten
```

> - NOTE: Make sure all paths in config and docker-compose volume do exist and sync together
> - NOTE: use `sudo docker-compose up -d` if root protected directories size are not accurate
> - Metrics is available at `:8000/metrics` path inside container
> - TIP: Use `find `pwd` -maxdepth 1 -type d` to get paths for all directories in current directory
