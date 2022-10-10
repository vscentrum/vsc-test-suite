echo "VSC Institute run file"

if [[ $@ != *"--mode="* ]]; then
  echo "Specify an execution mode via --mode=mymode"
  return 1 2>/dev/null
  exit 1
fi

module load ReFrame/3.12.0

export RFM_CONFIG_FILE=$(dirname $0)/config_vsc.py
export RFM_CHECK_SEARCH_PATH=$(dirname $0)/tests
export RFM_CHECK_SEARCH_RECURSIVE=true

reframe --run  "$@"
rm $(dirname $0)/*.out $(dirname $0)/*.log

report_dir=/apps/antwerpen/reframe/logs/reports

cat "$report_dir/last-$VSC_INSTITUTE_CLUSTER.json" >> "$report_dir/$VSC_INSTITUTE_CLUSTER.json"
echo -e '' >> "$report_dir/$VSC_INSTITUTE_CLUSTER.json"