import os
import reframe as rfm
import reframe.utility.sanity as sn
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from shared_fs_list import shared_fs, shared_fs_sites


@rfm.simple_test
class VSCSharedFSMountTest(rfm.RunOnlyRegressionTest):
    descr = "test shared filesystem mount point "
    fs = parameter(shared_fs.keys())
    site = parameter(shared_fs_sites)
    valid_systems = ["*:local", "*:single-node"]
    valid_prog_environs = ["builtin"]
    maintainers = ['rverschoren']
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"vsc", "cue", "fs"}

    @run_after('init')
    def set_param(self):
        path = os.path.join(shared_fs[self.fs]['mount'], self.site)
        self.descr += path
        exe = """python3 -c 'import os;print(os.path.isdir(os.path.realpath("{}")))'"""
        self.executable = exe.format(path)

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)


@rfm.simple_test
class VSCSharedFSMode(rfm.RunOnlyRegressionTest):
    descr = "test shared filesystem mode "
    fs = parameter(shared_fs.keys())
    site = parameter(shared_fs_sites)
    valid_systems = ["*:local", "*:single-node"]
    valid_prog_environs = ["builtin"]
    maintainers = ['rverschoren']
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"vsc", "cue", "fs"}

    @run_after('init')
    def set_param(self):
        path = os.path.join(shared_fs[self.fs]['mount'], self.site)
        self.descr += path
        mode = shared_fs[self.fs].get('mode')
        if not mode:
            # default: check if directory has rwxr-xr-x permissions 
            mode = '755'
        exe = """python3 -c 'import os;print(oct(os.stat(os.path.realpath("{}")).st_mode)[-3:] == "{}")'"""
        self.executable = exe.format(path, mode)

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)


@rfm.simple_test
class VSCSharedFSAccountDir(rfm.RunOnlyRegressionTest):
    descr = "test account directory "
    targets = []
    for x in shared_fs.keys():
        if 'envar' in shared_fs[x].keys():
            targets += [x]
    fs = parameter(targets)
    valid_systems = ["*:local", "*:single-node"]
    valid_prog_environs = ["builtin"]
    maintainers = ['rverschoren']
    time_limit = '10m'
    num_tasks = 1
    num_tasks_per_node = 1
    num_cpus_per_task = 1
    tags = {"vsc", "cue", "fs"}

    @run_after('init')
    def set_param(self):
        self.descr += shared_fs[self.fs]['mount'] + " " + shared_fs[self.fs]['envar'] + " " + os.environ['USER']
        path = os.environ[shared_fs[self.fs]['envar']]
        if not path:
            sites = {'1': "brussel", '2': "antwerpen", '3': "leuven", '4': "gent"}
            account_site = sites[os.environ["USER"][3]]
            path = os.path.join(shared_fs[self.fs]['mount'], account_site, os.environ['USER'][3:6], os.environ['USER'])
        exe = """python3 -c 'import os;print(os.path.isdir(os.path.realpath("{}")))'"""
        self.executable = exe.format(path)

    @sanity_function
    def assert_env(self):
        return sn.assert_found(r'^True$', self.stdout)
