import os
import time
import shutil
home = os.path.expanduser('~')
maindir = os.path.join(home, '.upk')
execdir = os.path.join(maindir, 'bin')
database = os.path.join(maindir, 'UPK.db')
packagesdir = os.path.join(maindir, 'packages')

cachedir = os.path.join(maindir, 'cache')
extractdir = os.path.join(cachedir, 'extract')
repocache = os.path.join(cachedir, 'repos')
lock = os.path.join(maindir, 'UPK.lock')
for i in [maindir, execdir, cachedir, extractdir, repocache, packagesdir]:
    os.makedirs(i, exist_ok=True)
if os.getenv('PATH'):
    path = os.getenv('PATH')
    path = path.strip().split(':')
    if execdir not in path:
        print("! warning")
        print(f"! upk is not in path, please add `export PATH=$PATH:{execdir}`")
        print("! to your .zshrc or .bashrc or your shell's configuration")
    
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
    for i in [cachedir, extractdir, repocache]:
        os.makedirs(i, exist_ok=True)

def clearextractCache():
    shutil.rmtree(extractdir)
    for i in [extractdir]:
        os.makedirs(i, exist_ok=True)
        