tools = [
    # {
    # 'exe': 'example command',
    # 'options': '--option -a 2>&1',    # works only when pkg not installed via rpm or skiprpm=True
    # 'minver': '93',
    # 're': r'(?<=\) )\d+',             # custom regex
    # 'skiprpm': True,                  # set to True to skip rpm check, which is usually preferred by the program
    # },
    {
        'exe': 'bash',
        'options': '--version',
        'minver': '4.2',
    },
    {
        'exe': 'ksh',
        'options': '--version 2>&1',
        'minver': '93',
        're': r'(?<=\) )\d+',
        'skiprpm': True,
    },
    {
        'exe': 'tcsh',
        'options': '--version',
        'minver': '6.18',
    },
    {
        'exe': 'zsh',
        'options': '--version',
        'modname': 'zsh',
        'minver': '5.0.2',
    },
    {
        'exe': 'screen',
        'options': '--version',
        'minver': '4.01',
    },
    {
        'exe': 'tmux',
        'options': '--version',
        'minver': '1.8',
    },
    {
        'exe': 'nano',
        'options': '--version',
        'minver': '2.2.6',
    },
    {
        'exe': 'vim',
        'options': '--version',
        'minver': '7.4',
    },
    {
        'exe': 'emacs',
        'options': '--version',
        'minver': '24',
    },
    {
        'exe': 'mc',
        'options': '--version',
        'minver': '4.8.7',
    },
    {
        'exe': 'svn',
        'options': '--version',
        'minver': '1.7.14',
    },
    {
        'exe': 'git',
        'options': '--version',
        'minver': '1.8.3',
    },
    {
        'exe': 'python3',
        'options': '--version',
        'minver': '3.6.8',
    },
    {
        'exe': 'perl',
        'options': '--version',
        'minver': '5.16.3',
    },
    {
        'exe': 'rsync',
        'options': '--version',
        'minver': '3.1.2',
    },
    {
        'exe': 'wget',
        'options': '--version',
        'minver': '1.14',
    },
    {
        'exe': 'curl',
        'options': '--version',
        'minver': '7.29',
    },
    {
        'exe': 'singularity',
        'options': '--version',
        'minver': '3.7.1',
    },
    {
        'exe': 'module',
        'options': '--version 2>&1',
        'minver': '8.2.7', 
    },
    {
        'exe': 'bzr',
        'options': '--version',
        'minver': '2.5.1',
        'modname': 'Bazaar',
        'skiprpm': True,
    },
    {
        'exe': 'hg',
        'options': '--version',
        'minver': '5.8',
        'modname': 'Mercurial',
        'skiprpm': True,
    },
    {
        'exe': 'python2',
        'options': '--version 2>&1',
        'minver': '2.7.18',
        'modname': 'Python/2.7.18-GCCcore-10.2.0',
        'skiprpm': True,
    },
    {
        'exe': 'smbclient',
        'options': '--version',
        'minver': '4.10.16',
        'modname': 'Samba',
        'skiprpm': True,
    },
    {
        'exe': 'eb',
        'options': '--version',
        'minver': '4.4.0',
        'modname': 'EasyBuild',
        'skiprpm': True,
    },
]
