import re


_import = re.compile(".*import(?:\s)*(?P<math>[a-zA-z0-9-_;]*)")
#_import_multiline = re.compile(".*import(?:\s)*(?:\\)(?:\\n)*(?:\s)*(?P<math>[a-zA-z0-9-_;]*)")
_from_import = re.compile(".*from(?:\s)*(?P<mod>[a-zA-z0-9-_;]*)(?:\s)*import(?:\s)*(?P<sub>[a-zA-z0-9-_;]*)")
_from_multiline = re.compile(".*(?:from(?:\s)*(?:\\{0,1})*(?:\s)*([\w_]*)(?:\s)*(?:\\{0,1})*(?:\s)*)?import\s*\\?\s*(?:\s*([\w_2]*)\s*,?)*;?$", re.I | re.M )

allowed_imports = [
    "math",
    "itertools",
    "collections",
]


def validate(script):
    print(_from_multiline.search(script))


def test():

    files = ["test_1.py"]


    for file in files:

        with open(file, "r") as f:
            script = f.read()

        result = validate(script)
        print(file, ":", "valid" if result else "invalid")




if __name__ == "__main__":
    test()
