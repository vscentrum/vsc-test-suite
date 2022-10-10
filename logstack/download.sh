singularity pull docker://grafana/promtail
singularity pull docker://grafana/grafana
singularity pull docker://grafana/loki
singularity pull docker://influxdb

singularity build --sandbox loki_sand loki_latest.sif
singularity build --sandbox grafana_sand grafana_latest.sif
singularity build --sandbox promtail_sand promtail_latest.sif
singularity build --sandbox influxdb_sand influxdb_latest.sif 

mkdir -p grafana/data loki/data loki/etc promtail/log promtail/etc influxdb2/data influxdb2/etc 

cd loki_sand/.singularity.d/
cp runscript startscript
cd ../../
#cp loki_sand/etc/loki/local-config.yaml loki/etc/
# config must be modified, use custom
cp local-config.yaml loki/etc/

cd grafana_sand/.singularity.d/
cp runscript startscript
cd ../../

cd promtail_sand/.singularity.d/
cp runscript startscript
cd ../../
#cp promtail_sand/etc/promtail/config.yml promtail/etc/
# Promtail config has to be modified in order to work, use custom
cp config.yml promtail/etc/

cd influxdb_sand/.singularity.d/
cp runscript startscript
cd ../../

singularity build loki_latest.sif loki_sand/
singularity build grafana_latest.sif grafana_sand/
singularity build promtail_latest.sif promtail_sand/
singularity build influxdb_latest.sif influxdb_sand/

rm -rf loki_sand grafana_sand promtail_sand influxdb_sand



