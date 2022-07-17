module load ReFrame/3.10.1

export RFM_CONFIG_FILE=$(dirname $0)/config_vsc.py
export RFM_CHECK_SEARCH_PATH=$(dirname $0)/tests
export RFM_OUTPUT_DIR=$HOME/reframe
export RFM_PREFIX=$HOME/reframe
export RFM_CHECK_SEARCH_RECURSIVE=true
export RFM_SAVE_LOG_FILES=true

reframe --run  "$@"