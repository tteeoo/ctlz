from ctlz import exceptions

def color(text, fg=None, bg=None):
    """Function to easily color printed text

    fg and bg kwargs can be set to any standard 4 bit terminal color, prefix with bright (as in 'bright_red') for the bright variant"""
    if fg == None and bg == None:
        return text
    elif fg == None:
        return "\033[{}m".format(__get_code(bg, mode="bg")) + text + "\033[0m"
    elif bg == None:
        return "\033[{}m".format(__get_code(fg)) + text + "\033[0m"
    else:
        return "\033[{};{}m".format(__get_code(fg), __get_code(bg, mode="bg")) + text + "\033[0m"

def underline(text):
    """Function to easily underline printed text"""
    return "\033[4m" + text + "\033[24m"

def blink(text):
    """Function to easily make printed text blink"""
    return "\033[5m" + text + "\033[25m"


def __get_code(color, mode="fg"):
    if color == "black":
        code = 30
    elif color == "red":
        code = 31
    elif color == "green":
        code = 32
    elif color == "yellow":
        code = 33
    elif color == "blue":
        code = 34
    elif color == "magenta":
        code = 35
    elif color == "cyan":
        code = 36
    elif color == "white":
        code = 37
    elif color == "bright_black":
        code = 90
    elif color == "bright_red":
        code = 91
    elif color == "bright_green":
        code = 92
    elif color == "bright_yellow":
        code = 93
    elif color == "bright_blue":
        code = 94
    elif color == "bright_magenta":
        code = 95
    elif color == "bright_cyan":
        code = 96
    elif color == "bright_white":
        code = 97
    else:
        raise exceptions.InvalidColor("No color " + color)

    if mode == "bg": code += 10
    return str(code)