# CUE Tests

## tools.py

This file contains tests which check the availability of a command and if it satisfies a minimum version requirement.

To add an extra command for both the tests edit the json `./src/tools_list.py`.
Each entry of a document is structured as follows:
* mandatory entries
    * `exe`: the actual command undergoing testing
* semi optional:
    * `minver`: the minimum accepted version of the specified command. Run will skip target VSCToolVersionTest if not present.
* optional entries
    * `veropt`: the version flag attached to the command, the default is `--version`
    * `options`: extra options postfixed to command and version flag
    * `re`: custom regular expression to extract the version number from the command output, default is `r'(?:(\d+\.(?:\d+\.)*\d+))'`
    * `modname`: load the specified module before executing the test. Packages requiring a module load in certain sites and are installed at system level in others can be handled by greedly adding the required module in this field.
    * `not_as_module`: default is False. If True, modname is mandatory in order to work. Check the inexistence of the module. Read msg from lmod in stderr.
    * `avail_on`: ['*:local',] list of systems/partitions where to perform the test, if not specified checks standard_partitions_tool_test global variable.
    * `negate`: default is False. If True, negates the result of the Availability test. Useful to check if something is not on the node image.

## env.py

The test executes checks on environment variables.

To add an extra variable edit the json `./src/envars_list.py`.
Each entry is structured as follows:
* mandatory entries
   * `name`: the actual variable
* optional entries
   * `exe`: the script executed by the test. The default script-string checks if envar exists and is not empty `"""python3 -c 'import os;print(os.environ["{}"] != "")'"""`. The inserted string will be then formatted: the variable name is identified by the brachets `{}` .

## shared_fs.py

This file contains tests which check the availability and mode of the shared file system and availability of account directories. 

To add an extra directory to test, edit the json `./src/shared_fs_list.py`.
Each entry of the document is structured as follows:
* mandatory entry
    * `mount`: the mount point/directory undergoing testing
* optional entry
    * `envar`: environment variable associated with the directory
