# unnamed Package Manager

A user-wide package manager written in python that is designed to be simple and easy-to-use

## Installation

Bootstrap upk to your system through

```bash
   bash -c (curl -fsSL https://raw.githubusercontent.com/juanvel4000/upk/HEAD/install.sh) 
```

    
## Packaging
Creating a package in upk is quite simple, you need a folder structure that looks like this
```tree
your-package
├── Info
│   └── Manifest.json
└── Source
    └── your-stuff
```
- Manifest.json: This manifest contains data about your package, it looks like this
```json
{
    "name": "libfoo",
    "version": "1.0",
    "binary": true,
    "summary": "foo librarier",
    "arch": "x86_64",
    "platform": "linux",
    "author": {
        "name": "johndoe",
        "mail": "johndoe@example.com"
    },
    "link": "https://example.com/johndoe/libfoo-1.0",
    "endpoints": {
        "example": "your-stuff"
    }
}
```
- name: the package name
- version: the package version
- binary: is the package a binary? set to true, otherwise false
- summary: a short description about your package
- arch: the architecture your package runs in, leave it as `any` to run on any machine
- platform: the platform your package runs on, can be `linux` or `darwin` (macOS)
- author->name: the name of the package publisher/maintainer
- author->mail: the public email of the package publisher/maintainer
- link: a link to the homepage of your project
- endpoints: a list of commands that point to objects on your package

Endpoints are basically symbolic links (symlinks) that are installed on `$HOME/.upk/bin` and serve as shortcuts to objects on your package 

## Repositories
Installing a package in upk is straightforward, you need to know two things
- the package name
- the package repository
You have to ensure that the package repository is on your repository list (repolist), to add a repository to your repolist, just run
```bash
upk repo add <name> <url>
```
once you added your package repository, to install a package, just run
```bash
upk install <repo>/<package>
```
where `<repo>` is the repository name you used when adding it, the default repository is [main](https://upk.juanvel400.xyz), and <package> is the name of the package you're installing
## Acknowledgements

 - Thanks to [Homebrew](https://brew.sh) for inspiration
## License

upk is licensed with [MIT](https://choosealicense.com/licenses/mit/), view `LICENSE`