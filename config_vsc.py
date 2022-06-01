import grp
import os

# use 'info' to log to syslog
syslog_level = 'warning'

perf_logging_format = 'reframe: ' + '|'.join(
    [
        'username=%(osuser)s',
        'version=%(version)s',
        'name=%(check_name)s',
        'system=%(check_system)s',
        'partition=%(check_partition)s',
        'environ=%(check_environ)s',
        'num_tasks=%(check_num_tasks)s',
        'num_cpus_per_task=%(check_num_cpus_per_task)s',
        'num_tasks_per_node=%(check_num_tasks_per_node)s',
        'modules=%(check_modules)s',
        'jobid=%(check_jobid)s',
        'perf_var=%(check_perf_var)s',
        'perf_value=%(check_perf_value)s',
        'unit=%(check_perf_unit)s',
    ]
)

# To run jobs on the kul cluster, you need to be a member of the following
# vsc group
kul_account_string_tier2 = '-A lpt2_vsc_test_suite'

# Specify hortense access flag in order to run jobs
# Flag is selected according to user group
hortense_access_flag = ''
groups = [grp.getgrgid(x).gr_name for x in os.getgroups()]
for admingroup in ['astaff', 'badmin', 'gadminforever', 'l_sysadmin']:
    if admingroup in groups:
        hortense_access_flag = f'-A {admingroup}'
        break

# Site Configuration
site_configuration = {
    'systems': [
        {
            'name': 'hydra',
            'descr': 'Hydra',
            'hostnames': ['login1.cerberus.os', 'login2.cerberus.os', '.*hydra.*'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'local',
                    'scheduler': 'local',
                    'modules': [],
                    'access': [],
                    'environs': ['builtin'],
                    'descr': 'tests in the local node (no job)',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'single-node',
                    'scheduler': 'slurm',
                    'modules': [],
                    'access': [],
                    'environs': ['builtin'],
                    'descr': 'single-node jobs',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'mpi-job',
                    'scheduler': 'slurm',
                    'access': [],
                    'environs': ['foss-2021a', 'builtin'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    'launcher': 'srun',
                },
            ]
        },
        {
            'name': 'hortense',
            'descr': 'VSC Tier-1 Hortense',
            'hostnames': ['login.*.dodrio.os'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'local',
                    'scheduler': 'local',
                    'modules': [],
                    'access': [],
                    'environs': ['builtin'],
                    'descr': 'tests in the local node (no job)',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'single-node',
                    'scheduler': 'slurm',
                    'modules': [],
                    'access': [hortense_access_flag],
                    'environs': ['builtin'],
                    'descr': 'single-node jobs',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'mpi-job',
                    'scheduler': 'slurm',
                    'access': [hortense_access_flag],
                    'environs': ['foss-2021a', 'builtin'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    # TODO Here we actually want to set vsc-mympirun, but since
                    # this is a custom launcher not shipped with ReFrame, we
                    # can only do this in the test itself after registering the
                    # vsc-mympirun launcher
                    'launcher': 'srun',
                },
            ]
        },
        {
            'name': 'genius',
            'descr': 'VSC Tier-2 Genius',
            'hostnames': ['tier2-p-login-[1-4].genius.hpc.kuleuven.be'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'local',
                    'scheduler': 'local',
                    'modules': [],
                    'access': [],
                    'environs': ['builtin'],
                    'descr': 'tests in the local node (no job)',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'single-node',
                    'scheduler': 'torque',
                    'modules': [],
                    'access': [kul_account_string_tier2],
                    'environs': ['builtin'],
                    'descr': 'single-node jobs',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'mpi-job',
                    'scheduler': 'torque',
                    'access': [kul_account_string_tier2],
                    'environs': ['builtin', 'foss-2021a'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    'launcher': 'mpirun',
                    'variables': [['MODULEPATH',
                                   ('/apps/leuven/skylake/2018a/modules/all:'
                                    '/apps/leuven/skylake/2021a/modules/all')
                                 ]],
                },
            ]
        },
        {
            'name': 'vaughan',
            'descr': 'VSC Tier-2 Vaughan',
            'hostnames': ['login[1-2].vaughan'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'local',
                    'scheduler': 'local',
                    'modules': [],
                    'access': [],
                    'environs': ['builtin'],
                    'descr': 'tests in the local node (no job)',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'single-node',
                    'scheduler': 'slurm',
                    'modules': [],
                    'access': [],
                    'environs': ['builtin'],
                    'descr': 'single-node jobs',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                                {
                    'name': 'mpi-job',
                    'scheduler': 'slurm',
                    'access': [],
                    'environs': ['intel-2021a', 'builtin'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    # TODO Here we actually want to set vsc-mympirun, but since
                    # this is a custom launcher not shipped with ReFrame, we
                    # can only do this in the test itself after registering the
                    # vsc-mympirun launcher
                    'launcher': 'srun',
                },
            ]
        },
    ],
    'environments': [
        {
            'name': 'builtin', 'cc': 'gcc', 'cxx': 'g++', 'ftn': 'gfortran',},
        {
            'name': 'foss-2021a', 'cc': 'mpicc', 'cxx': 'mpicxx',
            'ftn': 'mpif90', 'modules': ['foss/2021a'],},
        {   
            'name': 'intel-2021a',
            'modules': ['intel'],
            'cc': 'mpiicc',
            'cxx': 'mpiicpc',
            'ftn': 'mpiifort',
            'target_systems': ['vaughan']
        },
    ],
    'general': [
        {
            'purge_environment': True,
            'resolve_module_conflicts': False,  # avoid loading the module before submitting the job
            'keep_stage_files': True,
        }
    ],
    'logging': [
        {
            'level': 'debug',
            'handlers': [
                {
                    'type': 'file',
                    'name': 'reframe.log',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_name)s: %(message)s',  # noqa: E501
                    'append': False,
                },
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s',
                },
                {
                    'type': 'file',
                    'name': 'reframe.out',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': False,
                },
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': '%(check_job_completion_time)s ' + perf_logging_format,
                    'append': True,
                },
                {
                    'type': 'syslog',
                    'address': '/dev/log',
                    'level': syslog_level,
                    'format': perf_logging_format,
                    'append': True,
                },
            ],
        }
    ],
}
