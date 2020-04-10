import ctlz

app = ctlz.Control("calc> ", invalid_command="bad command")

@app.define("add * *")
def add():
    print(app.args)
    print(int(app.args[1]) + int(app.args[2]))

app.run()