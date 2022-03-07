tools = [
    # {
    # 'exe': 'command'                  # mandatory:    the command itself
    # 'veropt': '-V'                    # optional:     default = '--version'
    # 'options': '--option -a 2>&1',    # optional:     desired options as postfix 
    # 'minver': '93',                   # mandatory:    minimum version accepted 
    # 're': r'(?<=\) )\d+',             # optional:     custom regex for the command output if needed
    # 'modname': 'module'               # optional:     load the specified module 
    # },
    {
        'exe': 'bash',
        'minver': '4.2',
    },
    {
        'exe': 'ksh',
        'options': '2>&1',
        'minver': '93',
        're': r'(?<=\) )\d+',
    },
    {
        'exe': 'tcsh',
        'minver': '6.18',
    },
    {
        'exe': 'zsh',
        'modname': 'zsh',
        'minver': '5.0.2',
    },
    {
        'exe': 'screen',
        'minver': '4.01',
    },
    {
        'exe': 'tmux',
        'veropt': '-V',
        'minver': '1.8',
    },
    {
        'exe': 'nano',
        'minver': '2.2.6',
    },
    {
        'exe': 'vim',
        'minver': '7.4',
    },
    {
        'exe': 'emacs',
        'minver': '24',
    },
    {
        'exe': 'mc',
        'minver': '4.8.7',
    },
    {
        'exe': 'svn',
        'minver': '1.7.14',
    },
    {
        'exe': 'git',
        'minver': '1.8.3',
    },
    {
        'exe': 'python3',
        'minver': '3.6.8',
    },
    {
        'exe': 'perl',
        'minver': '5.16.3',
    },
    {
        'exe': 'rsync',
        'minver': '3.1.2',
    },
    {
        'exe': 'wget',
        'minver': '1.14',
    },
    {
        'exe': 'curl',
        'minver': '7.29',
    },
    {
        'exe': 'singularity',
        'minver': '3.7.1',
    },
    {
        'exe': 'ml',
        'options': '2>&1',
        'minver': '8.2.7', 
    },
    {
        'exe': 'bzr',
        'minver': '2.5.1',
        'modname': 'Bazaar',
    },
    {
        'exe': 'hg',
        'minver': '5.8',
        'modname': 'Mercurial',
    },
    {
        'exe': 'python2',
        'options': '2>&1',
        'minver': '2.7.18',
        'modname': 'Python/2.7.18-GCCcore-10.2.0',
    },
    {
        'exe': 'smbclient',
        'minver': '4.10.16',
        'modname': 'Samba',
    },
    {
        'exe': 'eb',
        'minver': '4.4.0',
        'modname': 'EasyBuild',
    },
]
