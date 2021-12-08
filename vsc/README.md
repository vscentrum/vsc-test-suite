# How to run the tests in the VUB cluster Hydra

```
module load ReFrame/3.9.1

export RFM_CONFIG_FILE=$PWD/config_hydra.py

reframe --verbose --run \
    --checkpath vsc.py \
    --setvar VSCEnvTest.valid_systems=hydra:local \
    --setvar VSCJobTest.valid_systems=hydra:single-node \
    --setvar valid_prog_environs=builtin
```


