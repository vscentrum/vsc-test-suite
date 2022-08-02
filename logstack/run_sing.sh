singularity instance start --bind grafana/data:/var/lib/grafana grafana_latest.sif grafana_server

singularity instance start --bind loki/data:/loki,loki/etc:/etc/loki/ loki_latest.sif loki_server

sleep 16

singularity instance start --bind promtail/log:/var/log,promtail/etc:/etc/promtail promtail_latest.sif promtail_server

singularity instance start --bind influxdb2/data/:/var/lib/influxdb2,influxdb2/etc:/etc/influxdb2 influxdb_latest.sif influxdb2_server
