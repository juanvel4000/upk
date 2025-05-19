import tarfile
import os
def compress(src, output):
    with tarfile.open(output, "w:xz") as tar:
        tar.add(src, arcname="")

def extract(src, output="."):
    with tarfile.open(src, "r:xz") as tar:
        tar.extractall(path=output)

def compress(workdir="."):
    if os.path.isdir(workdir):
        workdir = os.path.abspath(workdir)
    else:
        raise FileNotFoundError(f"directory: {workdir} does not exist")
    
    