envars = {
    'VSC_HOME':
    {
        'name': 'VSC_HOME',
        'exe': ['print(os.environ["USER"] in os.environ["{}"])'],
    },
    'VSC_DATA':
    {
        'name': 'VSC_DATA',
        'exe': ['print(os.environ["USER"] in os.environ["{}"])'],
    },
    'VSC_SCRATCH':
    {
        'name': 'VSC_SCRATCH',
        'exe': ['print(os.environ["USER"] in os.environ["{}"])'],
    },
    'VSC_ARCH_LOCAL':
    {
        'name': 'VSC_ARCH_LOCAL',
        # archspec is automatically installed as part of ReFrame
        'exe': [
            'import archspec.cpu',
            'arch = archspec.cpu.host().name',
            'archlist = [arch, arch.split("_")[0]]',  # relaxed spec, allows both skylake and skylake_avx512
            'print(os.environ["{}"] in archlist)',
        ],
    },
    'VSC_ARCH_SUFFIX':
    {
        'name': 'VSC_ARCH_SUFFIX',
        'exe': ['print(os.environ["{}"] in ["", "-ib"])'],
    },
    'VSC_INSTITUTE':
    {
        'name': 'VSC_INSTITUTE',
        'exe': ['print(os.environ["{}"] in ["antwerpen", "brussel", "gent", "leuven"])'],
    },
    'VSC_INSTITUTE_LOCAL':
    {
        'name': 'VSC_INSTITUTE_LOCAL',
        'exe': ['print(os.environ["{}"] in ["antwerpen", "brussel", "gent", "leuven"])'],
    },
    'VSC_INSTITUTE_CLUSTER':
    {
        'name': 'VSC_INSTITUTE_CLUSTER',
    },
    'VSC_OS_LOCAL':
    {
        'name': 'VSC_OS_LOCAL',
        'exe': ['print(os.environ["{}"] in ["CO7", "RHEL8", "centos8", "centos7"])'],
    },
    'VSC_SCRATCH_NODE':
    {
        'name': 'VSC_SCRATCH_NODE',
        'exe': ['print(os.environ["{}"] in ["/local", "/node_scratch", "/tmp"])'],
    },
    'VSC_SCRATCH_SITE':
    {
        'name': 'VSC_SCRATCH_SITE',
        'exe': ['print(os.environ["{}"] == os.environ["VSC_SCRATCH"])'],
    },
}
