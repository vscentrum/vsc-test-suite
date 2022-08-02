import grp
import os
import time

from py import builtin


standard_mode_options = [       
    '--exec-policy=async',
    '--strict',
    '--output=/apps/antwerpen/reframe/logs/output/',
    '--perflogdir=/apps/antwerpen/reframe/logs/',
    '--stage=/apps/antwerpen/reframe/logs/stage/',
    '--report-file=/apps/antwerpen/reframe/logs/reports/last-$VSC_INSTITUTE_CLUSTER.json',
    '--compress-report',
    '--nocolor']

perf_logging_format = [
        '{"username": "%(osuser)s"',
        '"version": "%(version)s"',
        '"name": "%(check_name)s"',
        '"system": "%(check_system)s"',
        '"partition": "%(check_partition)s"',
        '"environ": "%(check_environ)s"',
        '"nodelist": "%(check_job_nodelist)s"',
        '"num_tasks": "%(check_num_tasks)s"',
        '"num_cpus_per_task": "%(check_num_cpus_per_task)s"',
        '"num_tasks_per_node": "%(check_num_tasks_per_node)s"',
        '"modules": "%(check_modules)s"',
        '"jobid": "%(check_jobid)s"',
        '"perf_var": "%(check_perf_var)s"',
        '"perf_value": "%(check_perf_value)s"',
        '"unit": "%(check_perf_unit)s"',
        '"description": "%(check_descr)s"',
        '"end_time": "%(check_job_completion_time)s"',
    ]

logging_format = perf_logging_format + ['"message": "%(message)s"', '"time": "%(asctime)s"}']
perf_logging_format[-1] += '}'

# To run jobs on the kul cluster, you need to be a member of the following
# vsc group
kul_account_string_tier2 = '-A lpt2_vsc_test_suite'

# By default, not all installed modules are visible on the genius cluster
genius_modulepath = []
for version in ['2018a', '2019b', '2021a']:
    genius_modulepath.append(f'/apps/leuven/skylake/{version}/modules/all')

# Specify dodrio access flag in order to run jobs
# Flag is selected according to user group
dodrio_access_flag = ''
groups = [grp.getgrgid(x).gr_name for x in os.getgroups()]
for admingroup in ['astaff', 'badmin', 'gadminforever', 'l_sysadmin']:
    if admingroup in groups:
        dodrio_access_flag = f'-A {admingroup}'
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
                    'environs': ['foss-2021a'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    'launcher': 'srun',
                },
            ]
        },
        {
            'name': 'dodrio',
            'descr': 'VSC Tier-1 dodrio',
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
                    'access': [dodrio_access_flag],
                    'environs': ['builtin'],
                    'descr': 'single-node jobs',
                    'max_jobs': 1,
                    'launcher': 'local',
                },
                {
                    'name': 'mpi-job',
                    'scheduler': 'slurm',
                    'access': [dodrio_access_flag],
                    'environs': ['foss-2021a'],
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
                    'variables': [['MODULEPATH', ':'.join(genius_modulepath)]],
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
                    'variables': [['MODULEPATH', ':'.join(genius_modulepath)]],
                },
                {
                    'name': 'mpi-job',
                    'scheduler': 'torque',
                    'access': [kul_account_string_tier2],
                    'environs': ['foss-2021a'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    'launcher': 'mpirun',
                    'variables': [['MODULEPATH', ':'.join(genius_modulepath)]],
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
                    'environs': ['intel-2021a'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    # TODO Here we actually want to set vsc-mympirun, but since
                    # this is a custom launcher not shipped with ReFrame, we
                    # can only do this in the test itself after registering the
                    # vsc-mympirun launcher
                    'launcher': 'srun',
                },
                {
                    'name': 'nvidia',
                    'scheduler': 'slurm',
                    'access': ['-p ampere_gpu'],
                    'environs': ['CUDA', 'builtin'],
                    'descr': 'Nvidia ampere node',
                    'max_jobs': 1,
                    'launcher': 'srun',
                    'resources': [
                        {
                        'name': 'gpu',
                        'options': ['--gres=gpu:{num_gpus}'],
                        },
                    ]
                }
            ]
        },
        {
            'name': 'leibniz',
            'descr': 'VSC Tier-2 Leibniz',
            'hostnames': ['login[1-2].leibniz'],
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
                    'environs': ['intel-2021a'],
                    'descr': 'MPI jobs',
                    'max_jobs': 1,
                    # TODO Here we actually want to set vsc-mympirun, but since
                    # this is a custom launcher not shipped with ReFrame, we
                    # can only do this in the test itself after registering the
                    # vsc-mympirun launcher
                    'launcher': 'srun',
                },
                {
                    'name': 'nvidia',
                    'scheduler': 'slurm',
                    'access': ['-p pascal_gpu'],
                    'environs': ['CUDA', 'builtin'],
                    'descr': 'Nvidia pascal nodes',
                    'max_jobs': 2,
                    'launcher': 'srun',
                    'resources': [
                        {
                        'name': 'gpu',
                        'options': ['--gres=gpu:{num_gpus}'],
                        },
                    ]
                }
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
            #'target_systems': ['vaughan', 'leibniz']
        },
        {
            'name': 'CUDA',
            'modules': ['CUDA'],
            'cc': 'nvcc', 
            'cxx': 'nvcc', 
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
                    'name': '/apps/antwerpen/reframe/logs/log/$VSC_INSTITUTE_CLUSTER-reframe.log',
                    'level': 'debug2',
                    'format': ', '.join(logging_format),  # noqa: E501
                    'append': True,
                },
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s',
                },
                {
                    'type': 'file',
                    'name': '/apps/antwerpen/reframe/logs/output/$VSC_INSTITUTE_CLUSTER-reframe.out',
                    'level': 'info',
                    'format': '%(message)s',
                    'append': True,
                },
                        ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': 'performance/%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': ', '.join(perf_logging_format),
                    'append': True,
                },
            ],
        }
    ],
    'modes': [
        {
            'name': 'basic',
            'options': standard_mode_options + ['--tag=basic'],
        },
        {
            'name': 'numpy',
            'options': standard_mode_options + ['--tag=python'],
        },
        {
            'name': 'standard',
            'options': standard_mode_options + ['--exclude-tag=gpu'],
        },
        {
            'name': 'gpu',
            'options': standard_mode_options + ['--tag=gpu'],
        }
    ]
}
