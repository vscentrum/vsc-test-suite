import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class VSCJobTest(rfm.RunOnlyRegressionTest):
    descr = "test running job"
    valid_systems = ["*:single-node"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    executable = 'echo hello world!'
    tags = {"VSC", "micro"}

    @sanity_function
    def assert_job(self):
        return sn.assert_found(r'^hello world!$', self.stdout)
