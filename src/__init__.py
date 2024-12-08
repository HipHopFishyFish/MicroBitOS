"""
Driver code
"""


import main_os, games
# from microbit import *

main_os.login()

MENU = {
    0: main_os.off,          # OFF
    1: lambda : games.games_menu({    # GAMES
        0: lambda : games.falling_food(0),
        1: lambda : games.falling_food(1),
        2: lambda : games.falling_food(2)
    }),
}

main_os.menu(MENU)