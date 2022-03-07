py_start = "python3 -c 'import os;"

envars = [
    {
        'name': 'VSC_HOME',
        'exe': py_start  + """print(os.environ["USER"] in os.environ["{}"])'""",
    },
    {
        'name': 'VSC_DATA',
        'exe': py_start  + """print(os.environ["USER"] in os.environ["{}"])'""",
    },
    {
        'name': 'VSC_SCRATCH',
        'exe': py_start  + """print(os.environ["USER"] in os.environ["{}"])'""",
    },
    {
        'name': 'VSC_ARCH_LOCAL',
        # needs to have archspec python package installed
        # 'exe': "py_start  + """import archspec.cpu;print(archspec.cpu.host().name == os.environ["{}"])'""",
    },
    {
        'name': 'VSC_ARCH_SUFFIX',
        'exe': py_start  + """print(os.environ["{}"] in ["", "-ib"])'""",
    },
    {
        'name': 'VSC_INSTITUTE',
        'exe': py_start  + """print(os.environ["{}"] in ["antwerpen", "brussel", "gent", "leuven"])'""",
    },
    {
        'name': 'VSC_INSTITUTE_LOCAL',
        'exe': py_start  + """print(os.environ["{}"] in ["antwerpen", "brussel", "gent", "leuven"])'""",
    },
    {
        'name': 'VSC_INSTITUTE_CLUSTER',
    },
    {
        'name': 'VSC_OS_LOCAL',
        'exe': py_start  + """print(os.environ["{}"] in ["CO7", "RHEL8"])'""",
    },
    {
        'name': 'VSC_SCRATCH_NODE',
        'exe': py_start  + """print(os.environ["{}"] in ["/local", "/node_scratch", "/tmp"])'""",
    },
    {
        'name': 'VSC_SCRATCH_SITE',
        'exe': py_start  + """print(os.environ["{}"] == os.environ["VSC_SCRATCH"])'""",
    },
]
