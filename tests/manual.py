import ctlz

app = ctlz.Control("calc", prompt=ctlz.text.color("calcinator: ", fg="red"), global_flags=["-x"])

@app.define("add", params=["[0-9]", "[0-9]"], flags=["-m"])
def add():
    print(app.flags)
    print(int(app.params[0]) + int(app.params[1]))

@app.define("foo")
def foobar():
    print(app.flags)
    print("bar")

app.run()