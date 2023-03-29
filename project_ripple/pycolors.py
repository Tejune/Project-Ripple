def colors(red: int, green: int, blue: int):
    # return ansi escape code for the given color
    return f"\033[38;2;{red};{green};{blue}m"

# recreate colors but use a tuple instead of 3 arguments
def colort(args):
    return colors(*args)

def clear_color():
    # return ansi escape code to clear the color
    return "\033[0m"

# bold
bold = "\033[1m"
# italic
italic = "\033[3m"
# underline
underline = "\033[4m"
# strikethrough
strikethrough = "\033[9m"

#red
red = colors(200, 112, 112)
#green
green = colors(112, 200, 112)
#blue
blue = colors(112, 112, 200)
#yellow
yellow = colors(200, 200, 112)
#purple
purple = colors(200, 112, 200)
#cyan
cyan = colors(112, 200, 200)
#white
white = colors(255, 255, 255)
#black
black = colors(0, 0, 0)
#clear
clear = clear_color()