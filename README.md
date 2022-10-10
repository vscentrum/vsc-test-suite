# vsc-test-suite
VSC test suite

## How to run the tests

run script that works recursively

```
cd vsc-test-suite
./run.sh args
```

Optional `args` will be passed to the reframe command.

## VSC Run file

```
cd vsc-test-suite
./vsc_run.sh --mode=mymode
```

Uses the modes described in the `config_vsc.py` file.
- `basic`       runs only the basic hello world test
- `numpy`       runs only the 
- `standard`    runs all the tests but '-T intensive', '-T flexible' 

## Output location

Log files and output will be saved in $HOME/reframe

## Requirements 

- Reframe 3.12.0 installed as a module
- Python3
