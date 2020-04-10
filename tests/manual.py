import ctlz

config = ctlz.Config(["/home/theo/dev/repos/ctlz/tests/test.json"], "json")
print(config.deserialize())