import requests
from . import variables
import json
import os
def getIndex(srv):
    if srv not in getrepolist()['repositories']:
        print(f"fatal: server is not in your repository list, add {srv} to {variables.repolist}")
        return False
    res = requests.get(f'{getrepolist()['repositories'][srv]}/Index.json')
    if res.status_code != 200:
        return False
    return res.json()
def getRegistry(srv, pkg):
    if srv not in getrepolist()['repositories']:
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
def downloadPkg(registry, output=None, version="default"):
    if version not in registry['versions']:
        print(f"{registry['name']}::{version} not found")
        return False
    if output == None:
        output = os.path.join(variables.dldir, f'{registry['name']}-{registry['versions'][version]}.upk')
    if version == "default":
        default_version = registry['versions']['default']
        version = registry['versions'][default_version]

    else:
        version = registry['versions'][version]
    with requests.get(version, stream=True) as r:
        r.raise_for_status() 
        with open(output, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return output
def getrepolist():
    with open(variables.repolist, 'r') as repo:
        return json.load(repo)
