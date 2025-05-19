from . import package
from . import manifest
from . import variables
from . import database
import subprocess
import shutil
import os
import json
def installPkg(f):
    if not package.extract(f, variables.extractdir):
        return False
    Manifest = manifest.read(os.path.join(variables.extractdir, 'Info', 'Manifest.json'))
    db = database.Database()
    if db.isPackageInstalled(Manifest['name']):
        variables.clearextractCache()
        return False
    Filesdir = os.path.join(variables.extractdir, 'Source')
    dopost = False
    if 'scripts' in Manifest:
        if 'preinstall' in Manifest['scripts']:
            result = subprocess.run(["bash", Manifest['scripts']['preinstall']])
            if result.returncode != 0:
                print("preinstall failed")
                variables.clearextractCache()
                return False
        if Manifest['binary'] == False:
            Filesdir = os.path.join(variables.extractdir, 'Output')
            result = subprocess.run(["bash", Manifest['scripts']['build']])
            if result.returncode != 0:
                print("build failed")
                variables.clearextractCache()
                return False
        if 'postinstall' in Manifest['scripts']:
            dopost = True
    os.makedirs(os.path.join(variables.packagesdir, Manifest['name']), exist_ok=True)

    shutil.copytree(Filesdir, os.path.join(variables.packagesdir, Manifest['name']), dirs_exist_ok=True)
    if 'endpoints' in Manifest:
        for i in Manifest['endpoints']:
            src = os.path.join(variables.packagesdir, Manifest['name'], i)
            dst = os.path.join(variables.execdir, Manifest['endpoints'][i])
            if os.path.exists(dst) or os.path.islink(dst):
                os.remove(dst)
            os.symlink(src, dst)
    if dopost:
        result = subprocess.run(["bash", Manifest['scripts']['postinstall']])
        if result.returncode != 0:
            shutil.rmtree(os.path.join(variables.packagesdir, Manifest['name']))
            if 'endpoints' in Manifest:
                # delete endpoints
                for i in Manifest['endpoints']:
                    path = os.path.join(variables.execdir, i)
                    if os.path.exists(path) or os.path.islink(path):
                        os.remove(path)
            return False
    db.insertPackage(Manifest['name'], Manifest['version'], json.dumps(Manifest))
    return True

def removePkg(name):
    db = database.Database()
    if not db.isPackageInstalled(name):
        return False
    shutil.rmtree(os.path.join(variables.packagesdir, name))
    Manifest = json.loads(db.getPackageManifest(name))
    if 'endpoints' in Manifest:
        # delete endpoints
        for i in Manifest['endpoints']:
            path = os.path.join(variables.execdir, i)
            if os.path.exists(path) or os.path.islink(path):
                os.remove(path)

    db.deletePackage(name)
    return True
