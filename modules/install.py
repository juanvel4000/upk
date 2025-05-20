from . import package
from . import manifest
from . import variables
from . import database
import subprocess
import shutil
import os
import json
import uuid
def installPkg(f):
    print("initializing transaction")
    directory = os.path.join(variables.extractdir, f'{uuid.uuid4()}')
    os.makedirs(directory, exist_ok=True)
    if not package.extract(f, directory):
        return "could not extract package"
    Manifest = manifest.read(os.path.join(directory, 'Info', 'Manifest.json'))
    db = database.Database()
    if db.isPackageInstalled(Manifest['name']):
        variables.clearextractCache()
        return "package is already installed"
    Filesdir = os.path.join(directory, 'Source')
    dopost = False
    if 'scripts' in Manifest:
        if 'preinstall' in Manifest['scripts']:
            print("running pre install scripts")
            result = subprocess.run(["bash", os.path.join(directory, 'Scripts', Manifest['scripts']['preinstall'])])
            if result.returncode != 0:
                print("preinstall failed")
                variables.clearextractCache()
                return False
        if Manifest['binary'] == False:
            print("this is a source package")
            Filesdir = os.path.join(directory, 'Output')
            print("running build scripts")
            result = subprocess.run(["bash", os.path.join(directory, 'Scripts', Manifest['scripts']['build'])])
            if result.returncode != 0:
                print("build failed")
                variables.clearextractCache()
                return False
        if 'postinstall' in Manifest['scripts']:
            dopost = True
    os.makedirs(os.path.join(variables.packagesdir, Manifest['name']), exist_ok=True)

    shutil.copytree(Filesdir, os.path.join(variables.packagesdir, Manifest['name']), dirs_exist_ok=True)
    if 'endpoints' in Manifest:
        for endpoint, target in Manifest['endpoints'].items():
            src = os.path.join(variables.packagesdir, Manifest['name'], target)
            dst = os.path.join(variables.execdir, endpoint)
            if os.path.exists(dst) or os.path.islink(dst):
                os.remove(dst)
            print(f"installing symlink: {os.path.basename(dst)}")
            os.symlink(src, dst)

    if dopost:
        print("running post install scripts")
        result = subprocess.run(["bash", os.path.join(directory, 'Scripts', Manifest['scripts']['postinstall'])])
        if result.returncode != 0:
            print("postinstall failed")
            shutil.rmtree(os.path.join(variables.packagesdir, Manifest['name']))
            
            if 'endpoints' in Manifest:
                # delete endpoints
                for i in Manifest['endpoints']:
                    path = os.path.join(variables.execdir, i)
                    if os.path.exists(path) or os.path.islink(path):
                        os.remove(path)
            return False
    print("saving transaction")
    db.insertPackage(Manifest['name'], Manifest['version'], json.dumps(Manifest))
    return True

def removePkg(name):
    print("initializing transaction")
    db = database.Database()
    if not db.isPackageInstalled(name):
        return "package is not installed"
    print("removing the package data")
    shutil.rmtree(os.path.join(variables.packagesdir, name))
    Manifest = json.loads(db.getPackageManifest(name))
    if 'endpoints' in Manifest:
        # delete endpoints
        print("removing symlinks")
        for i in Manifest['endpoints']:
            path = os.path.join(variables.execdir, i)
            if os.path.exists(path) or os.path.islink(path):
                os.remove(path)
    print("saving transaction")
    db.deletePackage(name)
    return True
