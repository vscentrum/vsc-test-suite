import os
import reframe as rfm
import reframe.utility.sanity as sn
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from envars_list import envars

@rfm.simple_test
class VSCEnvTest(rfm.RunOnlyRegressionTest):
    descr = "test environment variable "
    envar = parameter(envars.keys())
    valid_systems = ["*:local", "*:single-node"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors", "Lewih"]
    tags = {"vsc", "cue"}

    @run_after('init')
    def set_param(self):
        self.descr += envars[self.envar]['name']
        exe = envars[self.envar].get('exe')
        if not exe:
            # default: check if envar exists and is not empty
            exe = """python3 -c 'import os;print(os.environ["{}"] != "")'"""
        self.executable = exe.format(envars[self.envar]['name'])

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)
