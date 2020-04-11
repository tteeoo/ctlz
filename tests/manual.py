import ctlz

app = ctlz.Control("calc", auto_help=True)

@app.define("add", params=[None])
def add():
    """Adds any amount of numbers provided as params"""

    total = 0
    for num in app.params:
        total += int(num)
    print(total)

app.run()