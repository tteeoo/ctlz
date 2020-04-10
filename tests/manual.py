import ctlz

app = ctlz.Control("calc")

@app.define("add", params=["[0-9]", "[0-9]"])
def add():
    print(int(app.params[0]) + int(app.params[1]))

@app.define(None)
def foobar():
    print("bar")

app.run()