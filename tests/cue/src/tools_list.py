standard_partitions_tool_test = ["*:local", "*:single-node"]


tools = {
    # 'testname':                           # mandatory: the name of the test
    # {
        # 'exe': 'command'                  # mandatory:    the command itself
        # 'veropt': '-V'                    # optional:     default = '--version'
        # 'options': '--option -a 2>&1',    # optional:     desired options as postfix 
        # 'minver': '93',                   # semi opti:    minimum version accepted, will skip VSCToolVersionTest if not present.
        # 're': r'(?<=\) )\d+',             # optional:     custom regex for the command output if needed
        # 'modname': 'module'               # optional:     load the specified module.
        # 'not_as_module': Bool             # optional:     if True, modname is mandatory in order to work. Check the inexistence of the module. Read msg from lmod in stderr.
        # 'avail_on': ['*:local',]          # optional:     list of systems/partitions where to perform the test, if not specified checks standard_partitions_tool_test.
        # 'negate': Bool                    # optional:     default is False. If True, negate the result of the Availability test.
    # },
    'bash':
    {
        'exe': 'bash',
        'minver': '4.2',
    },
    'ksh':
    {
        'exe': 'ksh',
        'options': '2>&1',
        'minver': '93',
        're': r'(?<=\) )\d+',
    },
    'tcsh':
    {
        'exe': 'tcsh',
        'minver': '6.18',
    },
    'zsh':
    {
        'exe': 'zsh',
        'minver': '5.0.2',
    },
    'screen':
    {
        'exe': 'screen',
        'minver': '4.01',
    },
    'tmux':
    {
        'exe': 'tmux',
        'veropt': '-V',
        'minver': '1.8',
    },
    'nano':
    {
        'exe': 'nano',
        'minver': '2.2.6',
    },
    'vim':
    {
        'exe': 'vim',
        'minver': '7.4',
    },
    'emacs':
    {
        'exe': 'emacs',
        'minver': '24',
    },
    'MidnightCommander':
    {
        'exe': 'mc',
        'minver': '4.8.7',
    },
    'subversion':
    {
        'exe': 'svn',
        'minver': '1.7.14',
    },
    'git':
    {
        'exe': 'git',
        'minver': '1.8.3',
    },
    'Python3':
    {
        'exe': 'python3',
        'minver': '3.6.8',
    },
    'Perl':
    {
        'exe': 'perl',
        'minver': '5.16.3',
    },
    'rsync':
    {
        'exe': 'rsync',
        'minver': '3.1.2',
        'avail_on': ['*:local']
    },
    'wget':
    {
        'exe': 'wget',
        'minver': '1.14',
        'avail_on': ['*:local']
    },
    'curl':
    {
        'exe': 'curl',
        'minver': '7.29',
        'avail_on': ['*:local']
    },
    'singularity':
    {
        'exe': 'singularity',
        'minver': '3.8.7',
    },
    'lmod':
    {
        'exe': 'ml',
        'options': '2>&1',
        'minver': '8.2.7', 
    },
    'bazaar':
    {
        'exe': 'bzr',
        'minver': '2.5.1',
        'modname': 'Bazaar',
    },
    'mercurial':
    {
        'exe': 'hg',
        'minver': '5.8',
        'modname': 'Mercurial',
    },
    'Python2':
    {
        'exe': 'python2',
        'options': '2>&1',
        'minver': '2.7.18',
        'modname': 'Python/2.7.18-GCCcore-10.2.0',
    },
    'Samba Client':
    {
        'exe': 'smbclient',
        'minver': '4.10.16',
        'modname': 'Samba',
        'avail_on': ['*:local']
    },
    'EasyBuild_module':
    {
        'exe': 'eb',
        'minver': '4.4.0',
        'modname': 'EasyBuild',
        'avail_on': ['*:local']
    },
    'EasyBuild_not_on_image':
    {
        'exe': 'eb',
        'negate': True
    },
    'ReFrame':
    {
        'exe': 'reframe',
        'minver': '3.10.1',
        'modname': 'ReFrame',
    },
    'Singularity_image_only':
    {
        'exe': 'singularity',
        'modname': 'Singularity',
        'not_as_module': True,
        'avail_on': ['*:local']
    },
    'Davix':
    {
        'exe': 'davix-cp',
        'minver': '0.7.6',
        'avail_on': ['*:local']
    },
    'iRODS':
    {
        'exe': 'icd',
        'minver': '4.2.8',
        'avail_on': ['*:local'],
        'veropt': '-h'
    },

}

