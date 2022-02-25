import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class VSCEnvTest(rfm.RunOnlyRegressionTest):
    descr = "test environment variable "
    envar = parameter(['VSC_HOME', 'VSC_DATA', 'VSC_SCRATCH'])
    valid_systems = ["*:local"]
    valid_prog_environs = ["*"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"antwerp"}

    @run_after('init')
    def set_param(self):
        self.descr += self.envar
        self.executable = f"""python3 -c 'import os;print(os.environ["USER"] in os.environ["{self.envar}"])'"""

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)
