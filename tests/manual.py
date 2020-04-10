import ctlz
mode = ctlz.Modes()
@mode.define("foo")
def bar():
    print("foobar")