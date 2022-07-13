import os
import reframe as rfm
import reframe.utility.sanity as sn
import sys

os.environ["TEST_ENVAR_OUTSIDE"] = 'defined'

@rfm.simple_test
class JobCleanEnvTest(rfm.RunOnlyRegressionTest):
    descr = "test that job starts in a clean environment"
    valid_systems = ["*:single-node"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors"]
    tags = {"vsc", "cue", "job"}
    exe = 'print(os.getenv("TEST_ENVAR_OUTSIDE") is None)'
    executable = f"python3 -c 'import os;{exe}'"

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)

@rfm.simple_test
class JobSrunCopyEnvTest(rfm.RunOnlyRegressionTest):
    descr = "test that srun inside job copies the job environment into the task environment"
    valid_systems = ["*:single-node"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors"]
    tags = {"vsc", "cue", "job"}
    prerun_cmds = ['export TEST_ENVAR_INSIDE=defined']
    exe = 'print(os.environ["TEST_ENVAR_INSIDE"] == "defined")'
    executable = f"srun python3 -c 'import os;{exe}'"

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)
