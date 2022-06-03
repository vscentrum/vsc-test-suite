import os
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher


# This test only passes if a reference performance target is attained. In case
# no reference value is available (e.g. when testing a new cluster or a new
# module), we fall back to a default value of 1s with no error margin. This
# can never be obtained, so the test will fail with a PerformanceError.
# Afterwards, the reference performance can be added based on the result of
# that run
default_performance_reference = {'time': (1.0, 0.0, 0.0, 's')}

performance_references = {
    (1, 'OpenFOAM/8-intel-2018a'): {
        'genius:mpi-job': {'time': (6178.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (4, 'OpenFOAM/8-intel-2018a'): {
        'genius:mpi-job': {'time': (1629.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (1, 'OpenFOAM/8-foss-2020a'): {
        'hydra:mpi-job': {'time': (6487.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (4, 'OpenFOAM/8-foss-2020a'): {
        'hydra:mpi-job': {'time': (1599.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (1, 'OpenFOAM/8-intel-2020a'): {
        'vaughan:mpi-job': {'time': (8490.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (4, 'OpenFOAM/8-intel-2020a'): {
        'vaughan:mpi-job': {'time': (2066.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (1, 'OpenFOAM/8-foss-2020b'): {
        # TODO This run on Hortense is very slow, probably because some built
        # in OpenFOAM script is used to launch a parallel run instead of
        # mympirun
        'hortense:mpi-job': {'time': (15506.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (4, 'OpenFOAM/8-foss-2020b'): {
        # TODO This run on Hortense does not complete, probably because some
        # built-in OpenFOAM script is used to launch a parallel run instead of
        # mympirun
        'hortense:mpi-job': {'time': (1.0, None, None, 's')},
        '*': default_performance_reference,
    },
    (1, 'OpenFOAM/8-intel-2020b'): {
        'hortense:mpi-job': {'time': (3848.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
    (4, 'OpenFOAM/8-foss-2020a'): {
        'hortense:mpi-job': {'time': (696.0, None, 0.1, 's')},
        '*': default_performance_reference,
    },
}

@rfm.simple_test
class OpenFOAMHPCMotorbikeTest(rfm.RunOnlyRegressionTest):
    descr = ''' '''
    valid_systems = ['*:mpi-job']
    valid_prog_environs = ['builtin']
    maintainers = ['stevenvdb']
    time_limit = '12h'
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
    elif cluster == 'dodrio':
        num_tasks_per_node = 128
        modules_to_test = parameter((
            ['OpenFOAM/8-foss-2020b'],
            ['OpenFOAM/8-intel-2020b'],
            ))
        job_options = []
    else:
        raise ValueError(f'VSC_INSTITUTE_CLUSTER={cluster} not supported')
    nnodes = parameter([1, 4])
    num_cpus_per_task = 1

    @run_after('setup')
    def set_resources(self):
        self.num_tasks = self.nnodes * self.num_tasks_per_node
        self.job.options = self.job_options

    @run_after('setup')
    def set_job_environment(self):
        self.modules = self.modules_to_test
        self.executable_opts = [f'{self.num_tasks}']
        # This test requires a few GB of temporary disk space. On most systems
        # $VSC_SCRATCH is a good candidate. On Hortense (dodrio) however,
        # quota on $VSC_SCRATCH is limited so we need another directory
        # TODO Find a place on dodrio accessible to all users of
        # vsc-test-suite, not only to Steven as is currently the case
        if self.cluster == 'dodrio':
            self.prerun_cmds = [
                "export REFRAME_SCRATCHDIR=/dodrio/scratch/projects/largescale_003/steven"
            ]
        else:
            self.prerun_cmds = [
                "export REFRAME_SCRATCHDIR=${VSC_SCRATCH}"
            ]

    @run_after('setup')
    def set_launcher(self):
        # mpirun is started inside OpenFOAM, so the job has to be launched
        # without mpirun
        self.job.launcher = getlauncher('local')()

    @run_after('setup')
    def set_performance_reference(self):
        self.strict_check = True
        # Get the performance reference for this combination of
        # (number of nodes, module). Fall back to default value if no entry
        # is available in the performance_references dictionary
        self.reference = performance_references.get(
            (self.nnodes, self.modules[0]), {'*': default_performance_reference})

    @sanity_function
    def check_steps_and_cells(self):
        # Check that the expected number of steps are executed
        pattern = r'^ExecutionTime = [0-9.]* s[ ]*ClockTime = (?P<clocktime>\S+) s$'
        self.clocktimes = sn.extractall(pattern, 'log.simpleFoam',
                                        'clocktime', float)
        check_number_of_steps = sn.assert_eq(sn.count(self.clocktimes), 500)

        # Check that the number of grid points is as expected
        pattern = r'^[\s]+cells:\s+(?P<cells>[0-9]+)$'
        cells = sn.extractsingle(pattern, 'log.checkMesh',
                                 'cells', int)
        # We cannot enforce equality, the number of cells slightly depends
        # on the number of processes. This check does avoid situations where
        # the number of cells is blatantly lower than 34M
        check_number_of_cells = sn.assert_ge(cells, 34000000)

        return sn.and_(check_number_of_steps, check_number_of_cells)

    @performance_function('s')
    def time(self):
        # Extract the last reported clockTime to get the time spent in actual
        # computation
        return self.clocktimes[-1]
