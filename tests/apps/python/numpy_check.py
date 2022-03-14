# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
from reframe.core.decorators import run_after
import reframe.utility.sanity as sn


@rfm.simple_test
class NumpyTest(rfm.RunOnlyRegressionTest):
    def __init__(self):
        self.descr = 'Test a few typical numpy operations'
        self.valid_prog_environs = ['builtin']
        self.modules = ['Python']
        
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
        self.tags = {'python', 'antwerp', 'performance'}
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
        }

    @run_after('setup')
    def set_num_cpus(self):
        self.num_cpus_per_task = 16
        self.variables = {
            'OMP_NUM_THREADS': str(self.num_cpus_per_task),
            'MKL_NUM_THREADS': str(self.num_cpus_per_task)
        }
