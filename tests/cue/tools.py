import os
from pkg_resources import parse_version as version
import reframe as rfm
import reframe.utility.sanity as sn
import sys

sys.path.append(os.path.dirname(__file__))
from tools_list import tools

@rfm.simple_test
class VSCToolAvailabilityTest(rfm.RunOnlyRegressionTest):
    descr = "test availability"
    tool = parameter(tools)
    valid_systems = ["*:local"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"antwerp"}

    @run_after('init')
    def set_param(self):
        self.descr += self.tool['exe']
        self.executable = f"""command -v {self.tool['exe']}"""
        if self.tool.get('modname'):
            self.executable = f"module load {self.tool['modname']} && " + self.executable

    @sanity_function
    def assert_availability(self):
        return sn.assert_found(r'^[a-zA-Z/]', self.stdout)


@rfm.simple_test
class VSCToolVersionTest(rfm.RunOnlyRegressionTest):
    descr = "test version"
    tool = parameter(tools)
    valid_systems = ["*:local"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"antwerp"}

    @run_after('init')
    def set_param(self):
        self.descr += self.tool['exe']
        self.executable = f"""python3 version_check.py {self.tool['exe']} {self.tool['minver']}"""
    @sanity_function
    def assert_availability(self):
        return sn.assert_found(r'^True$', self.stdout)

