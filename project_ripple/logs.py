from . import pycolors
import datetime, inspect, pathlib

name = "Project-Ripple"
def log(message, type, line):
    type = type.lower()
    match type:
        case "info":
            type = "   info"
            formatting = pycolors.blue + pycolors.bold
            message_color = pycolors.green
        case "warning":
            type = "warning"
            formatting = pycolors.yellow + pycolors.bold
            message_color = pycolors.colort((120, 120, 78))
        case "error":
            type = "  error"
            formatting = pycolors.red + pycolors.bold
            message_color = pycolors.colort((145, 112, 112))
        case "update":
            type = " update"
            formatting = pycolors.colort((121, 49, 180)) + pycolors.bold
            message_color = pycolors.colort((123, 42, 164))
    
    date = datetime.datetime.now().replace(microsecond=0)
    name = pathlib.Path(inspect.getframeinfo(line).filename).name
    print(f"{pycolors.bold}{pycolors.purple}{name} {pycolors.clear}{formatting}{type}{pycolors.cyan} →  {message_color}{message} @ {pycolors.colort((100,100,100))}{date} line {line.f_lineno}, {name} {pycolors.clear}")
