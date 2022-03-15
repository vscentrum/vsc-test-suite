tools = {
    # 'testname':                           # mandatory: the name of the test
    # {
        # 'exe': 'command'                  # mandatory:    the command itself
        # 'veropt': '-V'                    # optional:     default = '--version'
        # 'options': '--option -a 2>&1',    # optional:     desired options as postfix 
        # 'minver': '93',                   # mandatory:    minimum version accepted 
        # 're': r'(?<=\) )\d+',             # optional:     custom regex for the command output if needed
        # 'modname': 'module'               # optional:     load the specified module 
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
        'modname': 'zsh',
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
    },
    'wget':
    {
        'exe': 'wget',
        'minver': '1.14',
    },
    'curl':
    {
        'exe': 'curl',
        'minver': '7.29',
    },
    'singularity':
    {
        'exe': 'singularity',
        'minver': '3.7.1',
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
    },
    'EasyBuild':
    {
        'exe': 'eb',
        'minver': '4.4.0',
        'modname': 'EasyBuild',
    },
    'ReFrame':
    {
        'exe': 'reframe',
        'minver': '3.10.1',
        'modname': 'ReFrame',
    },
}
