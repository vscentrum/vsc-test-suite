import os
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import register_launcher
from reframe.core.launchers import JobLauncher
from reframe.core.backends import getlauncher


# TODO Ideally, this launcher would be included in the ReFrame repository. The
# next best thing is probably to define it in a script in vsc-test-suite that
# all tests can access.
@register_launcher('vsc-mympirun')
class MympirunLauncher(JobLauncher):
    def command(self, job):
        cmd = ['mympirun']
        if job.num_tasks_per_node:
            cmd += ['-h', str(job.num_tasks_per_node)]
        return cmd


@rfm.simple_test
class MPIHelloWorldTest(rfm.RegressionTest):
    descr = '''Compile and execute a simple Hello World MPI example. A job is
    launched on 2 nodes with 3 MPI processes per node. It is checked that each
    process prints a Hello World line and that indeed two nodes were used.'''
    valid_systems = ['*:mpi-job']
    valid_prog_environs = ['foss-2021a', 'intel-2021a']
    maintainers = ['stevenvdb']
    time_limit = '10m'
    num_tasks = 6
    num_tasks_per_node = 3
    num_cpus_per_task = 1
    executable = 'mpi_hello_world'
    sourcesdir = 'src_mpi_hello_world'
    tags = {"vsc", "micro", "mpi"}

    @run_before('run')
    def set_launcher_to_mympirun(self):
        if self.current_system.name in ['dodrio',]:
            self.modules += ['vsc-mympirun']
            self.job.launcher = getlauncher('vsc-mympirun')()

    @sanity_function
    def assert_number_of_hellos(self):
        # Check that the number of "Hello world" print statements equals the
        # total number of processes'''
        num_hellos = sn.len(sn.findall(r'^Hello world', self.stdout))
        num_hellos_ok = sn.assert_eq(num_hellos, self.num_tasks)

        # Check that the number of different hosts that printed "Hello world"
        # equals the number of nodes. The output contains lines like this:
        # Hello world from processor r25i27n07, rank 1 out of 6 processors
        # The regular expression extracts the part between processor and ,
        regex = r'^Hello world from processor (?P<node>\S+), rank'
        num_nodes = sn.count_uniq(sn.extractall(regex, self.stdout, 'node', str))
        num_nodes_ok = sn.assert_eq(num_nodes, self.num_tasks //
                                               self.num_tasks_per_node)
        return sn.assert_true(sn.and_(num_hellos_ok, num_nodes_ok))
