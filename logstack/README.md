# Log Stack 

This folder contains the scripts and config files necessary to setup the software stack which deals with reframe logs.

- the yaml files are the configuration files for loki(`local-config.yaml`) and promtail(`config.yml`) and include comments with references to the issues tracked on github.
- `download.sh` downloads the containers and configure the environment. The operation is not destructive and can be safely run to upgrade the containers.
- `run_sing.sh` runs the container instances and mounts the appropriate folders to the containers in order to give them persistency.
- `clean.sh` is a destructive script which resets loki db and promtail.
