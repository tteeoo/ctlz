import os
import ctlz

tracked = ctlz.Config([os.environ["HOME"] + "/.config/con/tracked.json"], "json", default={"con": os.environ["HOME"] + "/.config/con/config.json"})
tracked.deserialize()
config = ctlz.Config([os.environ["HOME"] + "/.config/con/config.json"], "json", default={"editor": "nvim", "colors": True}).deserialize()
app = ctlz.Control("con", auto_help=True)

@app.define("edit", params=[""], flags=["-s"])
def edit():
    try:
        if "-s" in app.flags: os.system("sudo " + config["editor"] + " " + tracked.data[app.params[0]])
        else: os.system(config["editor"] + " " + tracked.data[app.params[0]])
    except KeyError:
        print("con: no tracked nickname " + app.params[0])
    except:
        print("con: cannot access file " + tracked.data[app.params[0]])

@app.define("track", params=["", ""])
def track():
    tracked.data[app.params[0]] = app.params[1]
    tracked.serialize()

@app.define("untrack", params=[""])
def track():
    del tracked.data[app.params[0]]
    tracked.serialize()

@app.define(None)
def list_tracked():
    for nickname in list(tracked.data.keys()):
        print(nickname, tracked.data[nickname])

app.run()