import os
import reframe as rfm
import reframe.utility.sanity as sn
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from shared_fs_list import shared_fs


@rfm.simple_test
class VSCSharedFSMountTest(rfm.RunOnlyRegressionTest):
    descr = "test shared filesystem mount "
    fs = parameter(shared_fs)
    valid_systems = ["*:local", "*:single-node"]
    valid_prog_environs = ["builtin"]
    maintainers = ['rverschoren']
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"antwerp"}

    @run_after('init')
    def set_param(self):
        self.descr += self.fs['mount']
        exe = self.fs.get('exe')
        if not exe:
            # default: check if directory is a mount point
            exe = """python3 -c 'import os;print(os.path.ismount(os.path.realpath("{}")))'"""
        self.executable = exe.format(self.fs['mount'])

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)


@rfm.simple_test
class VSCSharedFSMode(rfm.RunOnlyRegressionTest):
    descr = "test shared filesystem mode "
    fs = parameter(shared_fs)
    valid_systems = ["*:local", "*:single-node"]
    valid_prog_environs = ["builtin"]
    maintainers = ['rverschoren']
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"antwerp"}

    @run_after('init')
    def set_param(self):
        self.descr += self.fs['mount']
        mode = self.fs.get('mode')
        if not mode:
            # default: check if directory has rwxr-xr-x permissions 
            mode = '755'
        exe = """python3 -c 'import os;print(oct(os.stat(os.path.realpath("{}")).st_mode)[-3:] == "{}")'"""
        self.executable = exe.format(self.fs['mount'], mode)

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)
