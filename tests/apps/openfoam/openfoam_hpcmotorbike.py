import os
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher


@rfm.simple_test
class OpenFOAMHPCMotorbikeTest(rfm.RunOnlyRegressionTest):
    descr = ''' '''
    valid_systems = ['*:mpi-job']
    valid_prog_environs = ['builtin']
    maintainers = ['stevenvdb']
    time_limit = '6h'
    executable = './run_openfoam_hpc_benchmark.sh'
    tags = {"vsc", "apps", "performance"}
    sourcesdir = 'sources'
    keep_files = ['log.simpleFoam', 'log.checkMesh']

    # Generate cluster specific cases
    cluster = os.environ['VSC_INSTITUTE_CLUSTER']
    if cluster == 'genius':
        num_tasks_per_node = 36
        modules_to_test = parameter((
            ['OpenFOAM/8-intel-2018a'],
            ))
        job_options = []
    elif cluster == 'vaughan':
        num_tasks_per_node = 36
        # On vaughan, git seems not available on compute nodes directly, so it
        # has to be loaded as a module
        modules_to_test = parameter((
            ['OpenFOAM/8-intel-2020a', 'git'],
            ))
        job_options = []
    elif cluster == 'hydra':
        num_tasks_per_node = 40
        modules_to_test = parameter((
            ['OpenFOAM/8-foss-2020a'],
            ))
        job_options = ["--partition=skylake_mpi"]
    elif cluster == 'hortense':
        num_tasks_per_node = 128
        modules_to_test = parameter((
            ['OpenFOAM/8-foss-2020a'],
            ['OpenFOAM/8-intel-2020a'],
            ))
        job_options = []
    else:
        raise ValueError(f'VSC_INSTITUTE_CLUSTER={cluster} not supported')
    nnodes = parameter([1])
    num_cpus_per_task = 1

    @run_after('setup')
    def set_resources(self):
        self.num_tasks = self.nnodes * self.num_tasks_per_node
        self.job.options = self.job_options

    @run_after('setup')
    def set_job_environment(self):
        self.modules = self.modules_to_test
        self.executable_opts = [f'{self.num_tasks}']

    @run_after('setup')
    def set_launcher(self):
        # mpirun is started inside OpenFOAM, so the job has to be launched
        # without mpirun
        self.job.launcher = getlauncher('local')()

    @sanity_function
    def check_number_of_steps(self):
        # Check that the expected number of steps are executed
        pattern = r'^ExecutionTime = [0-9.]* s[ ]*ClockTime = (?P<clocktime>\S+) s$'
        self.clocktimes = sn.extractall(pattern, 'log.simpleFoam',
                                        'clocktime', float)
        return sn.assert_eq(sn.count(self.clocktimes), 500)

    @sanity_function
    def check_number_of_grid_points(self):
         # Check that the number of grid points is as expected
         pattern = r'^[\s]+cells:\s+(?P<cells>[0-9]+)$'
         cells = sn.extractsingle(pattern, 'log.checkMesh',
                                  'cells', int)
         # We cannot enforce equality, the number of cells slightly depends
         # on the number of processes. This check does avoid situations where
         # the number of cells is blatantly lower than 34M
         return sn.assert_ge(cells, 34000000)

    @performance_function('s')
    def time(self):
        # Extract the last reported clockTime to get the time spent in actual
        # computation
        return self.clocktimes[-1]
