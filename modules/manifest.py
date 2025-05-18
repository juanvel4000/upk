import json
def read(f):
    with open(f, 'r') as manifest:
        m = json.dump(f)
        for attr in ["name", "author", "version", "binary", "summary"]:
            if attr not in i:
                raise SyntaxError(f"Missing key {attr} in {f}")
            if attr == "author":
                for attr2 in ['name', 'mail']:
                    if attr2 not in m['author']:
                        raise SyntaxError(f"Missing key author[{attr}] in {f}")
    return m