import json
def read(f):
    with open(f, 'r') as manifest:
        m = json.load(manifest)
        for attr in ["name", "author", "version", "binary", "summary", "arch", "platform"]:
            if attr not in m:
                raise SyntaxError(f"Missing key {attr} in {f}")
            if attr == "author":
                for attr2 in ['name', 'mail']:
                    if attr2 not in m['author']:
                        raise SyntaxError(f"Missing key author[{attr}] in {f}")
        if m['binary'] == False:
            if 'scripts' not in m:
                raise SyntaxError(f"Missing key scripts in {f}, binary is set false")
            if 'build' not in m['scripts']:
                raise SyntaxError(f"Missing key scripts['build'] in {f}, binary is set false")
    return m