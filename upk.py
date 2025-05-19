import modules
import sys
def _help():
    print("upk: unnamed package manager")
    print("upk is a user-wide package manager designed to manage upk packages (obviously)")
    print("commands:")
    print("install <file>           -   Install an upk package")
    print("remove <package>         -   Uninstall an upk package")
    print("build <workdir> [name]   -   Build an upk package")
    print("help                     -   Show this message")
def _main():
    argv = sys.argv[1:]
    argc = len(argv)
    if argc == 0:
        print("usage: upk <command>")
        sys.exit(1)
    match argv[0]:
        case 'install':
            if argc == 1:
                print("usage: upk install <file>")
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
                if argc == 2:
                    name = None
                else:
                    name = argv[1]
                modules.variables.waitLock()
                m = modules.package.compressPkg(workdir, name)
            except Exception as e:
                print(f"error: {e}")
            finally:
                modules.variables.delLock()
        case 'help':
            _help()
            sys.exit(1)
        case _:
            print("unknown command: " + argv[0])
            _help()
            sys.exit(1)
if __name__ == "__main__":
    _main()
