import tarfile

def compress(src, output):
    with tarfile.open(output, "w:xz") as tar:
        tar.add(src, arcname="")

def extract(src, output="."):
    with tarfile.open(src, "r:xz") as tar:
        tar.extractall(path=output)
