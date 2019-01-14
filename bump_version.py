

with open("wrapper/version.py", "r") as f:
    text = f.read().strip()

v=text.split("=")[1]
print("Current Version:", v)
v = v.split(".")
major = v[0]
minor = int(v[1])
minor += 1
new_v = "{}.{}".format(major, minor)
print("New Version:", new_v)

with open("wrapper/version.py", "w") as f:
    f.write("v={}".format(new_v))

