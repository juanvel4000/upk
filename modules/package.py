import tarfile
import os
from . import manifest
def compress(src, output):
    with tarfile.open(output, "w:xz") as tar:
        tar.add(src, arcname="")
    return True
def extract(src, output="."):
    with tarfile.open(src, "r:xz") as tar:
        tar.extractall(path=output)
    return True

def compressPkg(workdir=".", output=None):
    if os.path.isdir(workdir):
        workdir = os.path.abspath(workdir)
    else:
        raise FileNotFoundError(f"directory: {workdir} does not exist")
    if not os.path.isfile(os.path.join(workdir, 'Info', 'Manifest.json')):
        raise FileNotFoundError(f'cannot find {os.path.join(workdir, 'Info', 'Manifest.json')}')
    Manifest = manifest.read(os.path.join(workdir, 'Info', 'Manifest.json'))
    if Manifest['binary'] == False:
        if not os.path.isfile(os.path.join(workdir, 'Scripts', Manifest['scripts']['build'])):
            raise FileNotFoundError(f'cannot find {os.path.join(workdir, 'Scripts', Manifest['scripts']['build'])}')
    if 'scripts' in Manifest:
        for es in Manifest['scripts']:
            if not os.path.isfile(os.path.join(workdir, 'Scripts', Manifest['scripts'][es])):
                raise FileNotFoundError(f"cannot find {os.path.join(workdir, 'Scripts', Manifest['scripts'][es])}")
    # done checking
    if output == None:
        output = f"{Manifest['name']}-{Manifest['version']}.upk"
    return compress(workdir, output)
