
if [[ "$1" == "antwerp" ]]; then

    module use /apps/antwerpen/modules/centos8/software-admin-x86_64
    module load ReFrame/3.9.1

    export RFM_CONFIG_FILE=$PWD/config_vsc.py
    reframe --verbose --checkpath $PWD/tests --recursive --run

        
elif [[ "$1" == "ghent" ]]; then

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

elif [[ "$1" == "brussel" ]]; then

    module load ReFrame/3.9.1

    export RFM_CONFIG_FILE=$PWD/config_vsc.py

    reframe --verbose --run \
        --checkpath vsc.py \
        --setvar VSCEnvTest.valid_systems='hydra:local' \
        --setvar VSCJobTest.valid_systems='hydra:single-node' \
        --setvar valid_prog_environs='builtin'

else 
    echo "This never happens, add error or help message"
fi