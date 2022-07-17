echo "VSC Institute run file\n"

if [[ $@ != *"--mode="* ]]; then
  echo "Specify an execution mode via --mode=mymode"
  return 1 2>/dev/null
  exit 1
fi

module load ReFrame/3.10.1

export RFM_CONFIG_FILE=$(dirname $0)/config_vsc.py
export RFM_CHECK_SEARCH_PATH=$(dirname $0)/tests
export RFM_CHECK_SEARCH_RECURSIVE=true

reframe --run  "$@"
