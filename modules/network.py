import requests
from . import variables
def getIndex(srv):
    if srv not in getrepolist():
        print(f"fatal: server is not in your repository list, add {srv} to {variables.repolist}")
        return False
    res = requests.get(f'{srv}/Index.json')
    if res.status_code != 200:
        return False
    return res.json()
def getRegistry(srv, pkg):
    if srv not in getrepolist():
        print(f"fatal: server is not in your repository list, add {srv} to {variables.repolist}")
        return False
    index = getIndex(srv)
    if not index:
        return False
    if pkg in index['packages']:
        res = requests.get(index['packages'][pkg])
        if res.status_code != 200:
            return False
        return res.json()
def downloadPkg(registry, output=variables.dldir, version="default"):
    if version not in registry['versions']:
        print(f"{registry['name']}::{version} not found")
        return False
    with requests.get(registry['versions'][version], stream=True) as r:
        r.raise_for_status() 
        with open(output, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
def getrepolist():
    with open(variables.repolist, 'r') as repo:
        return repo.readlines()
