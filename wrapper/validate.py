import re


whitelist = [
    # builtin libraries
    "math",
    "itertools",
    "collections",
    "random",

    # engine specific
    "game.common.enums",
    "game.client.user_client",
]
_from = "from"
_import = "import"

def validate(script):
    results = []

    import_lines = []
    for line in script.split("\n"):
        if _import in line:
            import_lines.append(line.strip())


    for line_no,line in enumerate(import_lines):
        tokens = line.split()

        from_result = check_from(line_no+1, line, tokens)
        results.append(from_result)

        import_result = check_import(line_no+1, line, tokens)
        results.append(import_result)



    return sum(results) == len(results)



def check_from(line_no, line, tokens):
    result = True

    if _from in line:
        from_idx = tokens.index(_from)

        if len(tokens) <= from_idx+1:
            print("Line No {}: Split line \"from\" statements are not allowed".format(line_no))
            result = False


        module_name = tokens[from_idx+1]

        if module_name == "\\":
            print("Line No {}: Multiline imports are not allowed.".format(line_no, mod_name))
            result = False
        elif module_name not in whitelist:
            print("Line No {}: Import for module name \"{}\". Module not in whitelist. "\
                      "Remove illegal import.".format(line_no, module_name))
            result = False
    return result

def check_import(line_no, line, tokens):
    result = True

    if _import in line and _from not in line:

        import_idx = tokens.index(_import)
        for token in tokens[import_idx+1:]:

            mod_name = token.replace(",", "")
            mod_name = mod_name.replace(";", "")

            if mod_name == "\\":
                print("Line No {}: Multiline imports are not allowed.".format(line_no, mod_name))
                result = False
            elif mod_name not in whitelist:
                print("Line No {}: Import for module name \"{}\". Module not in whitelist. "\
                          "Remove illegal import.".format(line_no, mod_name))
                result = False

            if "," not in token:
                # end of list, we can exit
                break
    return result

def test():

    files = ["test_1.py"]


    for file in files:

        with open(file, "r") as f:
            script = f.read()

        result = validate(script)
        print(file, ":", result)


if __name__ == "__main__":
    test()
