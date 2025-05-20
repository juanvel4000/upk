import modules
import sys
import requests
import json
import platform
import os
import sys

if sys.version_info < (3, 11):
    print("upk requires python 3.11 or newer")
    sys.exit(1)

def _help():
    print("upk: unnamed package manager")
    print("upk is a user-wide package manager designed to manage upk packages (obviously)")
    print("commands:")
    print("install-local <file>                 -   Install an upk package")
    print("install <repo>/<pkg>[:version]       -   Install an upk package from a repository")
    print("remove <package>                     -   Uninstall an upk package")
    print("build <workdir> [name]               -   Build an upk package")
    print("help                                 -   Show this message")
    print("repo add <name> <url>                -   Add a new repository to your repository list")
    print("repo rm <name>                       -   Delete a repository from the repolist")
def resolve_dependencies(repo, pkg, version, resolved=None, seen=None):
    if resolved is None:
        resolved = []
    if seen is None:
        seen = set()

    key = f"{repo}/{pkg}:{version}"
    if key in seen:
        raise Exception(f"circular dependency detected: {key}")
    seen.add(key)

    reg = modules.network.getRegistry(repo, pkg)
    deps = reg.get("dependencies", {}).get(version, [])
    for dep in deps:
        dep_parts = dep.strip().split('/')
        dep_repo = dep_parts[0]
        pkg_ver = dep_parts[1].split(':')
        dep_pkg = pkg_ver[0]
        dep_ver = pkg_ver[1] if len(pkg_ver) > 1 else "default"
        resolve_dependencies(dep_repo, dep_pkg, dep_ver, resolved, seen)
        resolved.append((dep_repo, dep_pkg, dep_ver))  

    return resolved
def install_package(pkgstr):
    try:
        modules.variables.waitLock()

        c = pkgstr.strip().split('/')
        if len(c) != 2:
            print("usage: upk install <repo>/<pkg>[:version]")
            return False

        repo = c[0]
        parts = c[1].split(':')
        pkg = parts[0]
        ver = parts[1] if len(parts) > 1 and parts[1] else "default"

        if repo not in modules.network.getrepolist()['repositories']:
            print(f"error: repository '{repo}' is not added.")
            print(f"please run: upk repo add {repo} <url>")
            return False

        if pkg not in modules.network.getIndex(repo)['packages']:
            print(f"error: package '{pkg}' not found in repository '{repo}'")
            return False

        reg = modules.network.getRegistry(repo, pkg)
        if ver not in reg['versions']:
            print(f"error: version '{ver}' not listed in registry for {pkg}")
            return False

        arch, localplatform = reg['arch'], reg['platform']
        if arch not in ["any", platform.machine()]:
            print("error: this package does not run on your architecture")
            return False

        if localplatform != platform.system().lower():
            print(f"warning: this package is for {localplatform}, but you're using {platform.system()}")

        res = reg['versions'][ver]
        print(f"downloading {repo}/{pkg}:{ver}...")
        if modules.network.downloadPkg(reg, version=ver):
            print("package downloaded, installing...")
            output = os.path.join(modules.variables.dldir, f"{reg['name']}-{res}.upk")
        else:
            print("error: failed to download package")
            return False

        if os.path.isfile(output):
            modules.install.installPkg(output)
            return True
        else:
            print("error: downloaded file not found")
            return False

    except Exception as e:
        raise e
        return False
    finally:
        modules.variables.delLock()

def _main():
    argv = sys.argv[1:]
    argc = len(argv)
    if argc == 0:
        print("usage: upk <command>")
        sys.exit(1)
    match argv[0]:
        case 'install':
            if argc == 1:
                print("usage: upk install <repo>/<pkg>[:version]")
                sys.exit(1)
            success = install_package(argv[1])
            if not success:
                sys.exit(1)

        case 'install-local':
            if argc == 1:
                print("usage: upk install-local <file>")
                sys.exit(1)
            try:
                modules.variables.waitLock()
                m = modules.install.installPkg(argv[1])
                if m != True:
                    print(m)
            except Exception as e:
                 print(f"error: {e}")
            finally:
                modules.variables.delLock()
        case 'remove':
            if argc == 1:
                print("usage: upk remove <name>")
                sys.exit(1)
            try:
                modules.variables.waitLock()
                m = modules.install.removePkg(argv[1])
                if m != True:
                    print(m)
            except Exception as e:
                print(f"error: {e}")     
            finally:
                modules.variables.delLock() 
        case 'build':
            if argc == 1:
                print("usage: upk build <workdir> [package]")
                sys.exit(1)
            try:
                name = argv[2] if argc >= 3 else None
                modules.variables.waitLock()
                m = modules.package.compressPkg(argv[1], name)
            except Exception as e:
                print(f"error: {e}")
            finally:
                modules.variables.delLock()
        case 'help':
            _help()
            sys.exit(1)
        case 'clear':
            ca = modules.variables.clearCache()
            if not ca:
                print("error cleaning the cache")            
                sys.exit(1)
            else:
                print(" cache cleaned")
                sys.exit(1)
        case 'repo':
            if argc == 1:
                print("usage: upk repo <action>")
                sys.exit(1)
            match argv[1]:
                case 'add':
                    if argc == 2:
                        print("usage: upk repo add <name> <url>")
                        sys.exit(1)
                    if argc == 3:
                        print(f"usage: upk repo add {argv[2]} <url>")
                        sys.exit(1)
                    name = argv[2]
                    url = argv[3]
                    y = json.load(open(modules.variables.repolist, 'r'))
                    y['repositories'][name] = url
                    open(modules.variables.repolist, 'w').write(json.dumps(y))
                case 'rm':
                    if argc == 2:
                        print("usage: upk repo rm <name>")
                        sys.exit(1)
                    name = argv[2]
                    y = json.load(open(modules.variables.repolist, 'r'))
                    del y['repositories'][name]
                    open(modules.variables.repolist, 'w').write(json.dumps(y))
        case _:
            print("unknown command: " + argv[0])
            _help()
            sys.exit(1)
if __name__ == "__main__":
    _main()
