import os
from pkg_resources import parse_version as version
import reframe as rfm
import reframe.utility.sanity as sn
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from tools_list import tools

@rfm.simple_test
class VSCToolAvailabilityTest(rfm.RunOnlyRegressionTest):
    descr = "test command availability of "
    tool = parameter(tools.keys())
    valid_systems = ["*:local"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors", "Lewih"]
    tags = {"vsc", "cue", "tools"}

    @run_after('init')
    def set_param(self):
        self.descr += self.tool
        self.executable = f"""command -v {tools[self.tool]['exe']}"""
        modname = tools[self.tool].get('modname')
        if modname:
            self.modules = [modname]

    @sanity_function
    def assert_availability(self):
        return sn.assert_found(r'^[a-zA-Z/]', self.stdout)


@rfm.simple_test
class VSCToolVersionTest(rfm.RunOnlyRegressionTest):
    tool = parameter(tools.keys())
    valid_systems = ["*:local"]
    valid_prog_environs = ["builtin"]
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    maintainers = ["smoors", "Lewih"]
    tags = {"vsc", "cue", "tools"}

    @run_after('init')
    def set_param(self):
        ## dependency between tests
        variant = VSCToolAvailabilityTest.get_variant_nums(tool=lambda x: x==self.tool)
        self.depends_on(VSCToolAvailabilityTest.variant_name(variant[0]))

        self.descr = f"{self.tool} version >= {tools[self.tool]['minver']}"
        self.executable = f"""python3 version_check.py '{json.dumps(tools[self.tool])}' """
        modname = tools[self.tool].get('modname')
        if modname:
            self.modules = [modname]

    @sanity_function
    def assert_availability(self):
        return sn.assert_found(r'^True$', self.stdout)

