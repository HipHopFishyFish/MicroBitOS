from microbit import *
import time, random

GAMES_MENU_TEMPLATE = "{}\n00000\n50505\n00505\n00005"
FIRST_LINE_TEMPLATE = "{}0{}0{}"

FALLING_FOOD_TEMPLATE = "{}\n{}\n{}\n{}\n{}"

def _format_food_line(pos):
    return "{}{}{}{}{}".format(
        *["7" if i == pos else "0" for i in range(5)]
    )

def generate_games_menu(pos):
    display.clear()
    first_line = FIRST_LINE_TEMPLATE.format(*[9 if i == pos else 0 for i in range(3)])
    menu = GAMES_MENU_TEMPLATE.format(first_line)
    display.show(Image(menu))

def games_menu(games):
    time.sleep(0.3)
    pos = 1
    generate_games_menu(pos)

    while True:
        if button_a.is_pressed():
            pos -= 1 if pos > 0 else 0
            generate_games_menu(pos)
            time.sleep(0.2)
        if button_b.is_pressed():
            pos += 1 if pos < 2 else 0
            generate_games_menu(pos)
            time.sleep(0.2)
        if pin_logo.is_touched():
            display.clear()
            games[pos]()
            generate_games_menu(pos)

        if pin2.is_touched():
            display.clear()
            return

def _get_falling_food_board(pos, list):
    board = ""
    board_list = []
    for food_pos in list:
        if food_pos == -1:
            board_list.append("00000")
        else:
            board_list.append(_format_food_line(food_pos))

    board_list.append(_format_food_line(pos))
    board = FALLING_FOOD_TEMPLATE.format(*board_list)
    return board
            

def falling_food(difficulty):
    diff = {0: 8000, 1: 6500, 2: 5000}[difficulty]
    pos, game_time, since_last_button, full_time, score = 0, 0, 0, 0, 0
    uncollected = False
    food_list = [-1, -1, -1, -1]
    board = Image(_get_falling_food_board(pos, food_list))
    display.show(board)
    while True:
        full_time += 1
        game_time += 1
        since_last_button += 1
        if game_time == diff:
            uncollected = True
            game_time = 0
            food_list.insert(0, random.randint(0, 4))
            food_list.pop(4)
            board = Image(_get_falling_food_board(pos, food_list))
            display.show(board)

        if button_a.is_pressed() and since_last_button > 2000:
            since_last_button = 0
            pos -= 1 if pos > 0 else 0
            board = Image(_get_falling_food_board(pos, food_list))
            display.show(board)

        if button_b.is_pressed() and since_last_button > 2000:
            since_last_button = 0
            pos += 1 if pos < 4 else 0
            board = Image(_get_falling_food_board(pos, food_list))
            display.show(board)

        if pin2.is_touched():
            display.clear()
            time.sleep(0.2)
            return

        if pos == food_list[3] and uncollected:
            uncollected = False
            score += 1

        if full_time >= 400000:
            display.clear()
            time.sleep(0.5)
            display.scroll(score)
            return
            
            
            

    
            