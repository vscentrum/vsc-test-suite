# How to run the tests

## VUB Tier-2 cluster Hydra

```shell
module load ReFrame/3.9.1

export RFM_CONFIG_FILE=$PWD/config_vsc.py

reframe --verbose --run \
    --checkpath vsc.py \
    --setvar VSCEnvTest.valid_systems='hydra:local' \
    --setvar VSCJobTest.valid_systems='hydra:single-node' \
    --setvar valid_prog_environs='builtin'
```

## VSC Tier-1 Hortense (@ UGent)

```shell
# specify Slurm account to use (credits)
export SBATCH_ACCOUNT='gadminforever'

module load ReFrame/3.9.1
cd vsc-test-suite/vsc

export RFM_CONFIG_FILE=$PWD/config_vsc.py
reframe --verbose --run \
    --checkpath vsc.py \
    --setvar VSCEnvTest.valid_systems='hortense:local' \
    --setvar VSCJobTest.valid_systems='hortense:single-node' \
    --setvar valid_prog_environs='builtin'
```

## VSC Tier-2 Genius (@ KUL)

```shell
module load ReFrame/3.10.1
cd vsc-test-suite/vsc

export RFM_CONFIG_FILE=$PWD/config_vsc.py
reframe --verbose --run \
    --checkpath vsc.py \
    --setvar VSCEnvTest.valid_systems='genius:local' \
    --setvar VSCJobTest.valid_systems='genius:single-node' \
    --setvar valid_prog_environs='builtin'
```
