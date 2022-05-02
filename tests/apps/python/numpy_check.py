import reframe as rfm
from reframe.core.decorators import run_after
import reframe.utility.sanity as sn


@rfm.simple_test
class NumpyTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.descr = 'Test a few typical numpy operations'
        self.valid_prog_environs = ['builtin']
        self.modules = ['Python']
        self.time_limit = '20m'

        self.perf_patterns = {
            'dot': sn.extractsingle(
                r'^Dotted two \S* matrices in\s+(?P<dot>\S+)\s+s',
                self.stdout, 'dot', float),
            'svd': sn.extractsingle(
                r'^SVD of a \S* matrix in\s+(?P<svd>\S+)\s+s',
                self.stdout, 'svd', float),
            'cholesky': sn.extractsingle(
                r'^Cholesky decomposition of a \S* matrix in'
                r'\s+(?P<cholesky>\S+)\s+s',
                self.stdout, 'cholesky', float),
            'eigendec': sn.extractsingle(
                r'^Eigendecomposition of a \S* matrix in'
                r'\s+(?P<eigendec>\S+)\s+s',
                self.stdout, 'eigendec', float),
            'inv': sn.extractsingle(
                r'^Inversion of a \S* matrix in\s+(?P<inv>\S+)\s+s',
                self.stdout, 'inv', float),
        }

        self.sanity_patterns = sn.assert_found(r'Numpy version:\s+\S+',
                                               self.stdout)
        self.executable = 'python3'
        self.executable_opts = ['np_ops.py']
        # self.use_multithreading = False
        self.tags = {'apps', 'python', 'performance'}
        self.maintainers = ['Lewih']
        self.valid_systems = ['*:single-node']

        self.reference = {
            'vaughan:single-node': {
                'dot': (0.30, None, 0.10, 'seconds'),
                'svd': (0.55, None, 0.10, 'seconds'),
                'cholesky': (0.3, None, 0.10, 'seconds'),
                'eigendec': (7.0, None, 0.10, 'seconds'),
                'inv': (0.40, None, 0.10, 'seconds'),
            },
            'genius:single-node': {
                'dot': (0.46, None, 0.10, 'seconds'),
                'svd': (0.67, None, 0.10, 'seconds'),
                'cholesky': (0.15, None, 0.10, 'seconds'),
                'eigendec': (7.0, None, 0.10, 'seconds'),
                'inv': (0.22, None, 0.10, 'seconds'),
            },
            'hydra:single-node': {
                'dot': (0.25, None, 0.10, 'seconds'),
                'svd': (25.82, None, 0.10, 'seconds'),
                'cholesky': (0.77, None, 0.10, 'seconds'),
                'eigendec': (58.50, None, 0.10, 'seconds'),
                'inv': (0.54, None, 0.10, 'seconds'),
            },
            'hortense:single-node': {
                'dot': (1.28, None, 0.10, 'seconds'),
                'svd': (7.54, None, 0.10, 'seconds'),
                'cholesky': (0.58, None, 0.10, 'seconds'),
                'eigendec': (48.79, None, 0.10, 'seconds'),
                'inv': (1.31, None, 0.10, 'seconds'),
            },
        }

    @run_after('setup')
    def set_num_cpus(self):
        self.num_cpus_per_task = 6
        self.variables = {
            'OMP_NUM_THREADS': str(self.num_cpus_per_task),
            'MKL_NUM_THREADS': str(self.num_cpus_per_task)
        }

        if self.current_system.name == "hydra":
            self.modules.append("SciPy-bundle")
            self.job.options = ["--partition=skylake", "--exclusive", "--mem=0"]
        elif self.current_system.name == "hortense":
            self.modules.append("SciPy-bundle")
            self.job.options = ["--partition=skylake", "--exclusive", "--mem=0"]
