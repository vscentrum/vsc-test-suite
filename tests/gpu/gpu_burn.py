import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class GPU_Burn_nvidia(rfm.RunOnlyRegressionTest):
    descr = "GPU burn test on nvidia node"
    valid_systems = ["vaughan:nvidia"]
    valid_prog_environs = ["CUDA"]
    variables = {'CUDAPATH': '/apps/antwerpen/rome/centos8/CUDA/11.6.2'}
    time_limit = '10m'
    prebuild_cmds = ['git clone https://github.com/wilicc/gpu-burn.git']
    prerun_cmds = ['cd gpu-burn', 'make']
    executable = './gpu_burn 5'
    tags = {"antwerp", "gpu", "gpuburn"}

    def __init__(self):
        self.extra_resources = {'gpu': {'num_gpus': '4'}}

    @sanity_function
    def assert_job(self):
        return sn.and_(sn.assert_found(r'OK', self.stdout), sn.assert_not_found(r'FAULTY', self.stdout))
