import os
import reframe as rfm
import reframe.utility.sanity as sn

@rfm.simple_test
class GPU_Burn_nvidia(rfm.RunOnlyRegressionTest):
    descr = "GPU burn test on nvidia node"
    valid_systems = ["*:nvidia"]
    valid_prog_environs = ["CUDA"]
    modules = ['git']
    variables = {'CUDAPATH': '$EBROOTCUDA'}
    time_limit = '10m'
    prerun_cmds = ['git clone https://github.com/wilicc/gpu-burn.git', 'cd gpu-burn', 'make']
    executable = '--output=rfm_GPUBURN_nvidia_node-%N.out ./gpu_burn 20'
    tags = {"antwerp", "gpu", "burn"}
    num_devices = 0
    num_tasks_per_node = 1
    reference = {
        'vaughan:nvidia': {
            'device0': (17339.0, -0.05, 0.05, 'Gflop/s'),
            'device1': (17336.0, -0.05, 0.05, 'Gflop/s'),
            'device2': (17340.0, -0.05, 0.05, 'Gflop/s'),
            'device3': (17335.0, -0.05, 0.05, 'Gflop/s'),
        },
        'leibniz:nvidia': {
            'device0': (7412.0, -0.05, 0.05, 'Gflop/s'),
            'device1': (7412.0, -0.05, 0.05, 'Gflop/s'),
            'device2': (7412.0, -0.05, 0.05, 'Gflop/s'),
            'device4': (7412.0, -0.05, 0.05, 'Gflop/s'),
        }
    }

    @run_before('run')
    def set_options(self):
        if self.current_system.name == 'vaughan':
            self.num_devices = 4
            self.num_tasks = 1
        if self.current_system.name == 'leibniz':
            self.num_devices = 2
            self.num_tasks = 2
        
        self.extra_resources = {'gpu': {'num_gpus': str(self.num_devices)}}
        self.descr = f'Nvidia gpu burn test on {self.current_system.name} with {self.num_devices} gpus'

    @sanity_function
    def assert_job(self):
        result = True
        for n in sorted(self.job.nodelist):
            node = n.split('.')[0]
            result = sn.and_(sn.and_(sn.assert_found(r'OK', f'gpu-burn/rfm_GPUBURN_nvidia_node-{node}.out'), sn.assert_not_found(r'FAULTY', f'gpu-burn/rfm_GPUBURN_nvidia_node-{node}.out')), result)

        return result

    @performance_function('Gflop/s')
    def get_gflops(self, device=0, node=None):
        return sn.extractsingle(r'\((?P<gflops>\S+) Gflop/s\)', f'gpu-burn/rfm_GPUBURN_nvidia_node-{node}.out', 'gflops', float, item=(-device-1))

    @run_before('performance')
    def set_perf_variables(self):
        '''Build the dictionary with all the performance variables.'''
        self.perf_variables = {}

        counter = 0
        for n in sorted(self.job.nodelist):
            node =n.split('.')[0]
            for x in range(self.num_devices):
                self.perf_variables[f'device{counter}'] = self.get_gflops(device=self.num_devices-counter, node=node)
                counter += 1
