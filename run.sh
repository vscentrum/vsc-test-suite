export RFM_CONFIG_FILE=$(dirname $0)/config_vsc.py


if [[ "$1" == "antwerp" ]]; then

    module use /apps/antwerpen/modules/centos8/software-admin-x86_64
    module load ReFrame/3.9.1

    reframe --verbose --checkpath $(dirname $0)/tests --prefix $HOME --output $HOME --recursive --run


elif [[ "$1" == "ghent" ]]; then

    # specify Slurm account to use (credits)
    export SBATCH_ACCOUNT='gadminforever'

    module load ReFrame/3.9.1

    reframe --verbose --checkpath $(dirname $0)/tests --prefix $HOME --output $HOME --recursive --run


elif [[ "$1" == "brussel" ]]; then

    module load ReFrame/3.9.1

    reframe --verbose --checkpath $(dirname $0)/tests --prefix $HOME --output $HOME --recursive --run

elif [[ "$1" == "leuven" ]]; then

    module load ReFrame/3.10.1

    reframe --verbose --checkpath $(dirname $0)/tests --prefix $HOME --output $HOME --recursive --run
    
else 
    echo "This never happens, add error or help message"
fi
