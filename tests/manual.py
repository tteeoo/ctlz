import ctlz

app = ctlz.Control("calc", prompt=ctlz.text.color("calcinator: ", fg="red"), global_flags=["-x"], auto_help=True)

@app.define("add", params=["[0-9]", "[0-9]"], flags=["-m"])
def add():
    """Adds two numbers"""

    print(int(app.params[0]) + int(app.params[1]))

@app.define("foo")
@app.define("foooo")
def foobar():
    """Example"""

    print("bar")

app.run()