
import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher
import os


class GaussianBaseTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.valid_prog_environs = ['builtin']
        self.modules = ['Gaussian/g16_c01-avx2']

        self.sanity_patterns = sn.assert_found(r' Normal termination of Gaussian',
                                               self.stdout)
        self.perf_patterns = {
            'time': (
                sn.extractsingle(
                r'^real\t(?P<minutes>\S+)m\S+s',
                'rfm_GaussianCPUTest_job.err', 'minutes', float) + 
                sn.extractsingle(
                r'^real\t\S+m(?P<seconds>\S+)s',
                'rfm_GaussianCPUTest_job.err', 'seconds', float) / 60.0)
        }

        self.maintainers = ['Lewih']


@rfm.simple_test
class GaussianCPUTest(GaussianBaseTest):
    def __init__(self):
        super().__init__()
        self.valid_systems = ['leibniz:single-node',
                              'vaughan:single-node',
                              'hydra:single-node']
        self.reference = {
            'leibniz:single-node': {
                'time': (33.0, -0.5, 0.5, 'minutes/percentageOfMinute'),

            },
            'vaughan:single-node': {
                'time': (15.0, -0.05, 0.05, 'minutes/percentageOfMinute'),
                },
        }
        self.tags = {'apps', 'gaussian', 'performance'}


    @run_after('setup')
    def set_num_cpus(self):
        if self.current_system.name == 'leibniz':
            self.num_cpus_per_task = 28
        elif self.current_system.name == 'vaughan':
            self.num_cpus_per_task = 64
        elif self.current_system.name == 'hydra':
            self.num_cpus_per_task = 40
            self.job.options = ["--partition=skylake,skylake_mpi", "--exclusive"]
            self.modules = ['Gaussian/G16.B.01']

        self.executable = f'time g16 < mich-{self.current_system.name}.com'
    
        self.descr = f'Single Node Gaussian Test, cpus{self.num_cpus_per_task}'

    @run_before('run')
    def replace_launcher(self):
        self.job.launcher = getlauncher('local')()
