export RFM_CONFIG_FILE=$(dirname $0)/config_vsc.py
module load ReFrame/3.10.1

reframe --checkpath $(dirname $0)/tests --prefix $HOME/reframe --output $HOME/reframe --recursive --run  --save-log-files "$@"
rm $(dirname $0)/reframe.out $(dirname $0)/reframe.log
