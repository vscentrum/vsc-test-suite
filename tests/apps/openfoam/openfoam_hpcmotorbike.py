'''
OpenFOAM is free, open source software for CFD from the OpenFOAM Foundation.
The benchmark considered here is a variant of the Motorbike example shipped
with OpenFOAM, adapted to better suit typical usage of OpenFOAM in an HPC
environment. The input files are talken from the Large variant of the HPC
motorbike benchmark
(see https://develop.openfoam.com/committees/hpc/-/wikis/HPC-motorbike).

Before the actual CFD solver starts, the mesh has to be constructed. In
production runs, the mesh generation typically will only take small fraction
of the total wall time, and is therefore not part of the performance timings
in this test. The mesh generation has a large contribution to the runtime of
this test. So unfortunately, only a small portion is used to get performance
metrics.

The test currently runs using all available cores on a node as this is likely
how it would be used in production runs. Cases are generated for 1 and 4 full
nodes in order to study the internode scaling. Comparing timings for different
clusters is difficult because of the different core counts and the different
versions of OpenFOAM that are used.
As said before, directly comparing timings on different cluster is not easy.
Looking at the timings on 1 node, it seems that the Intel-based nodes of
genius (36 cores per node) and hydra-skylake (40 cores per node) offer a
better performance *per core* than the AMD-based nodes of vaughan (64 cores
per node) and Hortense (128 cores per node). Of course, the decision to do the
comparison on a *per core* basis is very debatable. These numbers then
probably just illustrate that on genius/hydra you get a higher-memory bandwidth
*per core*, which is of course beneficial for this memory-bound code.
On most clusters a superlinear speedup is observed when comparing the timings
on 1 full node and 4 full nodes. This has been reported before for OpenFOAM
and is most likely caused by the increase in availability and use of cache
memory when using more nodes, which again is very beneficial for a memory-bound
code like OpenFOAM. It is not yet clear why this is not the case on genius.

cluster     version         time 1 node     time 4 nodes        speedup
-----------------------------------------------------------------------
genius      8-intel-2018a          6178             1629            3.8
hydra       8-foss-2020a           6487             1599            4.1
vaughan     8-intel-2020a          8490             2066            4.1
hortense    8-intel-2020b          3848              696            5.5
'''

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
    (4, 'OpenFOAM/8-intel-2020b'): {
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
    tags = {"vsc", "apps", "performance", "resource-intensive"}
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
        num_tasks_per_node = 64
        # On vaughan, git seems not available on compute nodes directly, so it
        # has to be loaded as a module
        modules_to_test = parameter((
            ['OpenFOAM/8-intel-2020a', 'git'],
            ))
        job_options = []
    elif cluster == 'leibniz':
        num_tasks_per_node = 28
        # On leibniz, git seems not available on compute nodes directly, so it
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

    def __init__(self):
        self.tags.add(f"{self.nnodes}nodes")

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
        if self.cluster == 'dodrio':
            self.prerun_cmds = [
                "# Find an appropriate scratch dir accessible to current user",
                "for ADMINGROUP in astaff badmin gadminforever l_sysadmin; do",
                "    if [ -w ${VSC_SCRATCH_PROJECTS_BASE}/${ADMINGROUP} ]; then",
                "        export REFRAME_SCRATCHDIR=${VSC_SCRATCH_PROJECTS_BASE}/${ADMINGROUP}",
                "    fi",
                "done",
                "if [ -z ${REFRAME_SCRATCHDIR+x} ]; then",
                "    echo 'Could not find appropriate scratch directory'",
                "    exit 1",
                "fi",
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
