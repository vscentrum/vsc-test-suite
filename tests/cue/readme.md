# CUE Tests

## tools.py

This file contains 2 tests which check the availability of a command and if it satisfies a minimum version requirement.

To add an extra command for both the tests edit the json `./src/tools_list.py`.
Each entry of the document is structured as follows:
* mandatory entries
    * `exe`: the actual command undergoing testing
    * `minver`: the minimum accepted version of the specified command
* optional entries
    * `version_opt`: the version flag attached to the command, the default is `--version`
    * `options`: extra options postfixed to command and version flag
    * `re`: custom regular expression to extract the version number from the command output, default is `r'(?:(\d+\.(?:\d+\.)*\d+))'`
    * `modname`: load the specified module before executing the test. Packages requiring a module load in certain sites and are installed at system level in others can be handled by greedly adding the required module in this field. 

## env.py