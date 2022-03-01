import os
import reframe as rfm
import reframe.utility.sanity as sn

tools = {
    'bash': '4.2',
    'ksh': '93',
    'tcsh': '6.18',
    'zsh': '5.0.2',
    'screen': '4.01',
    'tmux': '1.8',
    'nano': '2.2.6',
    'vim': '7.4',
    'emacs': '24',
    'mc': '4.8.7',
    'svn': '1.7.14',
    'git': '1.8.3',
    'python3': '3.6.8',
    'perl': '5.16.3',
    'rsync': '3.1.2',
    'wget': '1.14',
    'curl': '7.29',
    'singularity': '3.7.1',
    'module': '8.2.7',
}

@rfm.simple_test
class VSCToolAvailabilityTest(rfm.RunOnlyRegressionTest):
    descr = "test availability"
    envar = parameter(list(tools.keys()))
    valid_systems = ["*:local"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"antwerp"}

    @run_after('init')
    def set_param(self):
        self.descr += self.envar
        self.executable = f"""{self.envar} --version"""

    @sanity_function
    def assert_env(self):
        return sn.assert_not_found(r'command not found', self.stderr)
