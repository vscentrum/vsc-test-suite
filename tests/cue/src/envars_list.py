py_start = "python3 -c 'import os;"

envars = {
    'VSC_HOME':
    {
        'name': 'VSC_HOME',
        'exe': py_start  + """print(os.environ["USER"] in os.environ["{}"])'""",
    },
    'VSC_DATA':
    {
        'name': 'VSC_DATA',
        'exe': py_start  + """print(os.environ["USER"] in os.environ["{}"])'""",
    },
    'VSC_SCRATCH':
    {
        'name': 'VSC_SCRATCH',
        'exe': py_start  + """print(os.environ["USER"] in os.environ["{}"])'""",
    },
    'VSC_ARCH_LOCAL':
    {
        'name': 'VSC_ARCH_LOCAL',
        # needs to have archspec python package installed
        # 'exe': "py_start  + """import archspec.cpu;print(archspec.cpu.host().name == os.environ["{}"])'""",
    },
    'VSC_ARCH_SUFFIX':
    {
        'name': 'VSC_ARCH_SUFFIX',
        'exe': py_start  + """print(os.environ["{}"] in ["", "-ib"])'""",
    },
    'VSC_INSTITUTE':
    {
        'name': 'VSC_INSTITUTE',
        'exe': py_start  + """print(os.environ["{}"] in ["antwerpen", "brussel", "gent", "leuven"])'""",
    },
    'VSC_INSTITUTE_LOCAL':
    {
        'name': 'VSC_INSTITUTE_LOCAL',
        'exe': py_start  + """print(os.environ["{}"] in ["antwerpen", "brussel", "gent", "leuven"])'""",
    },
    'VSC_INSTITUTE_CLUSTER':
    {
        'name': 'VSC_INSTITUTE_CLUSTER',
    },
    'VSC_OS_LOCAL':
    {
        'name': 'VSC_OS_LOCAL',
        'exe': py_start  + """print(os.environ["{}"] in ["CO7", "RHEL8", "centos8", "centos7"])'""",
    },
    'VSC_SCRATCH_NODE':
    {
        'name': 'VSC_SCRATCH_NODE',
        'exe': py_start  + """print(os.environ["{}"] in ["/local", "/node_scratch", "/tmp"])'""",
    },
    'VSC_SCRATCH_SITE':
    {
        'name': 'VSC_SCRATCH_SITE',
        'exe': py_start  + """print(os.environ["{}"] == os.environ["VSC_SCRATCH"])'""",
    },
}
