import os
import time
import shutil
home = os.path.expanduser('~')
maindir = os.path.join(home, '.upk')
execdir = os.path.join(maindir, 'bin')
database = os.path.join(maindir, 'UPK.db')
packagesdir = os.path.join(maindir, 'packages')
repolist = os.path.join(maindir, 'repos')
cachedir = os.path.join(maindir, 'cache')
extractdir = os.path.join(cachedir, 'extract')
repocache = os.path.join(cachedir, 'repos')
lock = os.path.join(maindir, 'UPK.lock')
dldir = os.path.join(cachedir, 'downloads')
for i in [maindir, execdir, cachedir, extractdir, repocache, packagesdir, dldir]:
    os.makedirs(i, exist_ok=True)
if os.getenv('PATH'):
    path = os.getenv('PATH')
    path = path.strip().split(':')
    if execdir not in path:
        print("! warning")
        print(f"! upk is not in path, please add `export PATH=$PATH:{execdir}`")
        print("! to your .zshrc or .bashrc or your shell's configuration")
if not os.path.isfile(repolist):
    with open(repolist, 'w') as re:
        re.write('')
def setLock():
    global lock
    with open(lock, 'w') as l:
        l.write('')
def checkLock():
    global lock
    return os.path.isfile(lock)
def delLock():
    global lock
    return os.remove(lock)
def waitLock():
    if checkLock():
        timewaiting = 0
        while os.path.isfile(lock):
            print(f'\rtime waiting for lock {timewaiting} (if you are sure that no upk is running, remove {lock})', end="")
            time.sleep(1)
            timewaiting += 1
    setLock()
    return True

def clearCache():
    shutil.rmtree(cachedir)
    for i in [cachedir, extractdir, repocache, dldir]:
        os.makedirs(i, exist_ok=True)
    return True
def clearextractCache():
    if os.path.exists(extractdir):
        shutil.rmtree(extractdir)
    os.makedirs(extractdir, exist_ok=True)
