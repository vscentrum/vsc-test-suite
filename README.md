# vsc-test-suite
VSC test suite

## How to run the tests

run script that works recursively

```
cd vsc-test-suite
./run.sh args
```

Optional `args` will be passed to the reframe command.

## Output location

Log files and output will be saved in $HOME

## Requirements 

- Reframe 3.10.1 installed as a module
- Python3

## TODOs

- --prefix is set to $HOME/reframe in order to not have conflicts between different users (write permissions of log files mainly). needs improvement.
