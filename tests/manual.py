import ctlz

app = ctlz.Control("calc", prompt=ctlz.text.color("calcinator: ", fg="red"), global_flags=["-x"], auto_help=True)

@app.define("add", params=[None])
def add():
    """Adds some numbers"""
    total = 0
    for num in app.params:
        total += int(num)
    print(total)

@app.define("foo")
@app.define("foooo")
def foobar():
    """Example"""

    print("bar")

app.run()