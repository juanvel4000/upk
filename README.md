
# upk
![Static Badge](https://img.shields.io/badge/upk_Version-0.2-blue)

upk is a minimalistic package manager written in Shell Script




## Features

- **Compression**: Uses **LZMA** (_xz_) and **Tape Archiver** (_tar_) for compression
- **Cross-platform**: Since its a Shell Script, it can run in any **Unix-like** System


## Installation

Clone the repository, and install it with Tools like `install`

```bash
  git clone https://github.com/juanvel4000/upk
  cd upk
  install -m 755 upk /usr/local/bin/upk
```
## Dependencies
- **sha256sum**: For Package Authenticity
- **awk**: For Creating a **sha256** sum 
- **tar**: For extraction and compression
- **xz**: For extraction and compression

## Usage/Examples
**Create a package:**
```bash
mkdir -p package/{UPK,usr,usr/bin}
touch package/usr/bin/hello
echo "echo \"Hello World!\"" >> package/usr/bin/hello
chmod +x package/usr/bin/hello
upk build manifest package
upk build scan "$(pwd)/package"
mkdir output
upk build build "$(pwd)/package" "mypackage" "$(pwd)/output"

```
Install that package, test it, and remove it
```bash
upk install "$(pwd)/output/mypackage-1.00-any.upk"
hello
upk remove "mypackage"
```
## License
UPK Is Licensed with the `MIT/X11` License, view `upk license` or `LICENSE`.
## Changelog
For a changelog, view **CHANGELOG.md**