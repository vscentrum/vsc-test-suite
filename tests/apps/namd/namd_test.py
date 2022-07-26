import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.backends import getlauncher


class NamdBaseTest(rfm.RunOnlyRegressionTest):
    num_nodes = parameter(['1', '2', '4', ])

    def __init__(self, arch):
        self.descr = f'NAMD check on {arch}, number of nodes: {self.num_nodes}, apoa1 and stmv(4 nodes only)'
        # fallback module load
        self.modules = ['NAMD']

        self.sanity_patterns = sn.assert_found(r'WRITING EXTENDED SYSTEM TO OUTPUT FILE AT STEP',
                                               self.stdout)
        self.perf_patterns = {
            'days_ns': sn.avg(sn.extractall(
                r'Info: Benchmark time: \S+ CPUs \S+ '
                r's/step (?P<days_ns>\S+) days/ns \S+ MB memory',
                self.stdout, 'days_ns', float))
        }

        self.maintainers = ['Lewih']

        self.tags = {'apps', 'namd', 'performance'}
        self.tags.add(f'{self.num_nodes}nodes')

    @run_before('run')
    def replace_launcher(self):
        self.job.launcher = getlauncher('local')()

    def download_material(self):
        if int(self.num_nodes) in {1, 2}:
            self.prerun_cmds = [
                'wget https://www.ks.uiuc.edu/Research/namd/utilities/apoa1.zip', 'unzip apoa1.zip']
            return "apoa1"
        if int(self.num_nodes) > 2:
            self.prerun_cmds = [
                'wget https://www.ks.uiuc.edu/Research/namd/utilities/stmv.zip', 'unzip stmv.zip']
            return "stmv"

    def create_nodelist(self):
        # scheduler commands
        if self.current_system.name == 'genius':
            # torque prerun commands
            self.prerun_cmds += ['echo Number of nodes: $PBS_NP',
                                 'for node in `cat $PBS_NODEFILE`; do echo host $node >>mynodes; done']
        else:
            # slurm prerun commands
            self.prerun_cmds += ['echo Number of nodes: $SLURM_NPROCS',
                                 'for node in `scontrol show hostnames`; do echo host $node >>mynodes; done']


@rfm.simple_test
class Namd_SMP_CPUTest(NamdBaseTest):
    # NAMD SMP CPU test

    def __init__(self):
        self.tags.add('smp')
        self.time_limit = '20m'

        self.valid_systems = ['leibniz:single-node',
                              'vaughan:single-node',
                              'genius:single-node', ]
        self.valid_prog_environs = ['builtin']
        super().__init__('cpu')

        self.scale_reference = {
            '1': {
                'leibniz:single-node': {'days_ns': (0.345, None, 0.05, 'days/ns')},
                'vaughan:single-node': {'days_ns': (0.1991375, None, 0.05, 'days/ns')},
            },
            '2': {
                'leibniz:single-node': {'days_ns': (0.24671949, None, 0.05, 'days/ns')},
                'vaughan:single-node': {'days_ns': (0.1601965, None, 0.05, 'days/ns')},
            },
            '4': {
                'leibniz:single-node': {'days_ns': (1.317, None, 0.05, 'days/ns')},
                'vaughan:single-node': {'days_ns': (0.7218169, None, 0.05, 'days/ns')},
            },
        }
        self.reference = self.scale_reference[self.num_nodes]

    @run_after('setup')
    def set_num_cpus(self):
        self.num_tasks = int(self.num_nodes)

        configFile = self.download_material()

        # VSC specific config
        if self.current_system.name == 'leibniz':
            self.num_cpus_per_task = 28
            self.modules = ['NAMD/2.14-verbs-smp']
        elif self.current_system.name == 'vaughan':
            self.num_cpus_per_task = 64
            self.modules = ['NAMD/2.14-verbs-smp']
        elif self.current_system.name == 'genius':
            self.num_cpus_per_task = 36
            self.modules = ['NAMD/2.14-foss-2019b-mpi']

        self.create_nodelist()

        self.executable = f'charmrun +p {self.num_cpus_per_task*self.num_tasks} $EBROOTNAMD/namd2 {configFile}/{configFile}.namd'


@rfm.simple_test
class Namd_NotSMP_CPUTest(NamdBaseTest):
    # NAMD notSMP CPU test

    def __init__(self):
        self.time_limit = '20m'

        self.valid_systems = ['leibniz:single-node',
                              'vaughan:single-node',
                              'genius:single-node',
                              'hydra:single-node']

        self.valid_prog_environs = ['builtin']
        super().__init__('cpu')

        self.scale_reference = {
            '1': {
                'leibniz:single-node': {'days_ns': (0.347779, None, 0.05, 'days/ns')},
                'vaughan:single-node': {'days_ns': (0.188093, None, 0.05, 'days/ns')},
                'hydra:single-node': {'days_ns': (0.207591, None, 0.05, 'days/ns')},
            },
            '2': {
                'leibniz:single-node': {'days_ns': (0.1782715, None, 0.05, 'days/ns')},
                'vaughan:single-node': {'days_ns': (0.09856985, None, 0.05, 'days/ns')},
                'hydra:single-node': {'days_ns': (0.1704705, None, 0.05, 'days/ns')},
            },
            '4': {
                'leibniz:single-node': {'days_ns': (1.05726, None, 0.05, 'days/ns')},
                'vaughan:single-node': {'days_ns': (0.5438339, None, 0.05, 'days/ns')},
                'hydra:single-node': {'days_ns': (4.24083, None, 0.05, 'days/ns')},
            },
        }
        self.reference = self.scale_reference[self.num_nodes]

    @run_after('setup')
    def set_num_cpus(self):
        self.num_tasks = int(self.num_nodes)

        configFile = self.download_material()

        launcher = 'charm'

        # VSC specific config
        if self.current_system.name == 'leibniz':
            self.num_cpus_per_task = 28
            self.modules = ['NAMD/2.14-verbs']
        elif self.current_system.name == 'vaughan':
            self.num_cpus_per_task = 64
            self.modules = ['NAMD/2.14-verbs']
        elif self.current_system.name == 'hydra':
            self.num_tasks = 40 * self.num_tasks
            self.modules = ['NAMD/2.14-foss-2019b-mpi']
            self.job.options = ["--partition=skylake,skylake_mpi",
                                "--exclusive", f"--nodes={int(self.num_nodes)}"]
            launcher = 'mpi'
        elif self.current_system.name == 'genius':
            self.num_cpus_per_task = 36
            self.modules = ['NAMD/2.14-foss-2019b-mpi']

        self.create_nodelist()

        # select launcher
        if launcher == 'charm':
            self.executable = f'charmrun +p {self.num_cpus_per_task*self.num_tasks} $EBROOTNAMD/namd2 {configFile}/{configFile}.namd'
        if launcher == 'mpi':
            self.executable = f'srun $EBROOTNAMD/namd2 {configFile}/{configFile}.namd'
