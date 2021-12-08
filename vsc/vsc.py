import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class VSCEnvTest(rfm.RunOnlyRegressionTest):
    descr = "test environment variable "
    envar = parameter(['VSC_HOME', 'VSC_DATA', 'VSC_SCRATCH'])
    valid_systems = required
    valid_prog_environs = required
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1

    @run_after('init')
    def set_description(self):
        self.descr += self.envar

    @run_after('init')
    def set_executable(self):
        self.executable = f"""python3 -c 'import os;print(os.environ["USER"] in os.environ["{self.envar}"])'"""

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)

@rfm.simple_test
class VSCJobTest(rfm.RunOnlyRegressionTest):
    descr = "test running job"
    valid_systems = required
    valid_prog_environs = required
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    executable = 'echo hello world!'

    @sanity_function
    def assert_job(self):
        return sn.assert_found(r'^hello world!$', self.stdout)
