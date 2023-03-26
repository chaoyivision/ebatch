class tcolor:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def get_timestamp():
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%y%m%d-%H%M%S")

def randomize_codebase_id():
    from random_word import RandomWords
    return f'{get_timestamp()}-{RandomWords().get_random_word()}'

def build_patterns(includes, excludes):
    from fnmatch import fnmatch, filter
    from os.path import isdir, join

    """Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """
    def _ignore_patterns(path, names):
        keep = set(name for pattern in includes
                            for name in filter(names, pattern))


        ignores = []
        for name in names:
            fullname = path + '/' + name
            for e in excludes:
                if e in name:
                    ignores.append(name)

            if name not in keep and not isdir(join(path, name)):
                ignores.append(name)
            
        ignores = set(ignores)
        return ignores
    return _ignore_patterns

def snapshot_codebase(src, dst, includes= ['*.py', '*.txt', '*.md', '*.yaml', '*.zsh'], excludes=['wandb', '.pyc', '__pycache__', '.vscode']):
    from shutil import copytree
    import time, shutil, errno

    start = time.time()
    print('snapshooting current codebase: ')
    print(f'      * from {src}')
    print(f'      * to   {tcolor.BOLD}{dst}{tcolor.END}')
    print(f'      + first includes: {includes}')
    print(f'      - then  excludes: {excludes}')
    
    
    try:
        shutil.copytree(src, dst, ignore=build_patterns(includes, excludes))
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise
    print(f'      * took {int(time.time()-start)}s')



def overwrite_sbatch_cfg(cfg, placeholder, value, template):
    if value is not None: 
        cfg = cfg.replace(placeholder, template + str(value))
    else:
        cfg = cfg.replace(placeholder, '')
    return cfg





def random_sbatch_script_path():
    import tempfile, getpass, os
    from datetime import date
    # initial easy_batch script is created within /tmp
    tmpdir = os.path.join(tempfile.gettempdir(), 'easy_sbatch-' + getpass.getuser())
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    (_, file_script) = tempfile.mkstemp(prefix=str(date.today()) + '_', suffix='.slurm', dir=tmpdir)
    return file_script

def create_folder_if_not_exists(p):
    import os
    if not os.path.exists(p):
        os.makedirs(p)