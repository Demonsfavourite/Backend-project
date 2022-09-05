import random as r
import time
import sweeperlib as s
timing = time.strftime("%d.%m.%Y %H:%M", time.localtime())
time_start = time.time()
statistics = {
                
                "time": timing,
                "duration": time_start,
                "number_of_transfers": 0,
                "game_situation": "",
                "field_length": 0,
                "field_height": 0,
                "add_mines": 0,
                "game_over": False
            }

def mines(field, free_frames, add_mines):
    while add_mines > 0:
        size = len(free_frames) - 1
        rand = r.randint(0, size)
        x, y = free_frames[rand][:]
        field[y][x] = "x"
        free_frames.remove(free_frames[rand])
        add_mines = add_mines - 1

def create_field():
    while True:
        try:
            length = int(input("Enter the field length: "))
            if length < 5 or length > 100:
                print("Field length must be a minimum of 5 and a maximum of 100")
                raise ValueError
            height = int(input("Enter the height of the field: "))
            if height < 5 or height > 100:
                print("The field height is a minimum of 5 and a maximum of 100")
                raise ValueError
            add_mines = int(input("Enter the number of mines: "))
            if add_mines < 1 or add_mines >= length * height:
                print("The number of mines is a minimum of 1 and is limited")
                raise ValueError
            break
        except ValueError:
            print("Value Error!")

    field = []
    for row in range(height):
        field.append([])
        for column in range(length):
            field[-1].append(" ")

    left = []
    for x in range(length):
        for y in range(height):
            left.append((x, y))

    mines(field, left, add_mines)

    statistics["field_height"] = height
    statistics["field_length"] = length
    statistics["add_mines"] = add_mines

    return field

def check_coordinates(x, y, width, height):
    try:
        if x < 0 or y < 0:
            raise TypeError
        elif 0 <= x < width and 0 <= y < height:
            return True
        else:
            return False
    except TypeError:
        return False

def count_mines(x, y, field):
    total = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if check_coordinates(j, i, len(field[1]), len(field)):
                if field[i][j] == "x":
                    total = total + 1
    return total

def floodfill(field, x, y):
    list = [(x, y)]
    if field[y][x] == " ":
        while len(list) > 0:
            coordinates = list.pop()
            x = int(coordinates[0])
            y = int(coordinates[1])
            if count_mines(x, y, field) == 0:
                field[y][x] = "0"
            else:
                field[y][x] = str(count_mines(x, y, field))
                continue
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if i < 0:
                        i = 0
                    if j < 0:
                        j = 0
                    if j > len(field[0]) - 1:
                        j = len(field[0]) - 1
                    if i > len(field) - 1:
                        i = len(field) - 1
                    if field[i][j] == " ":
                        length = j
                        height = i
                        new = (length, height)
                        list.append(new)

def game_logic(x1, y1):
    if check_coordinates(x1, y1, len(field[1]), len(field)):
        if field[y1][x1] == " ":
            if count_mines(x1, y1, field) == 0:
                floodfill(field, x1, y1)
            else:
                field[y1][x1] = str(count_mines(x1, y1, field))

        if empty(field):
            print("Congratulations! You won the game!")
            statistics["game_situation"] = "Win"
            statistics["game_over"] = True
            s.set_mouse_handler(bibek)

        if field[y1][x1] == "x":
            field[y1][x1] = "m"
            print("You lost the game!")
            statistics["game_over"] = True
            statistics["game_situation"] = "Lost"
            s.set_mouse_handler(bibek)

def handle_mouse(x, y, button, pressed):
    if button == s.MOUSE_LEFT:
        x1 = int(x / 40)
        y1 = int(y / 40)
        statistics["number_of_transfers"] = statistics["number_of_transfers"] + 1
        game_logic(x1, y1)

def save_statistics(statistics):
    with open("Minesweeper.txt", "a") as file:
        file.write("\nGame Time: {} \nGame Duration: {} \nNumber of Transfers: {} \n"
                       "Game Status: {} \nField Size: {} x {} \nNumber of Mines: {} \n".format(
            statistics["time"],
            statistics["duration"], statistics["number_of_transfers"], statistics["game_situation"],
            statistics["field_length"], statistics["field_height"], statistics["add_mines"]))

def load_statistics():
    with open("Minesweeper.txt") as file:
        data = file.read()
        print(data)

def empty(field): 
    for i in field:
        for j in i:
            if j == " ":
                return
    return True

def bibek(x, y, handle, edit):
    time_up = time.time()
    statistics["duration"] = time.strftime("%M min %S s", time.gmtime(time_up - time_start))
    if s.MOUSE_LEFT:
        save_statistics(statistics)
        s.close()        

def draw_field():
    s.clear_window()
    s.draw_background()
    s.begin_sprite_draw() 
    y = -40
    for i in field:
        y = y + 40
        x = - 40
        for j in i:
            x = x + 40
            s.prepare_sprite(" ", x, y)
            if j == "f":
                s.prepare_sprite("f", x, y)
            if j == "m":
                s.prepare_sprite("x", x, y)
            for k in range(9):
                k = str(k)
                if k == j:
                    s.prepare_sprite(k, x, y)
            if statistics["game_over"]:
                if j in ('x', 'm'):
                    s.prepare_sprite("x", x, y)
    s.draw_sprites()

def main(field):
    s.load_sprites("sprites")
    width = len(field[1]) * 40
    height = len(field) * 40
    s.create_window(width, height)
    s.set_draw_handler(draw_field)
    s.set_mouse_handler(handle_mouse)
    s.start() 

if __name__ == "__main__":
    while True:
        try:
            print("1 Start a new game \n2 View stats \n3 Quit")
            selection = int(input("Choose the option you want using the number: "))
            if selection == 1:
                statistics["game_over"] = False
                field = create_field()
                field.reverse()
                main(field)
            elif selection == 2:
                load_statistics()
            elif selection == 3:
                break
            else:
                raise ValueError
        except ValueError:
            print("Please type 1, 2, or 3!")
        except FileNotFoundError:
            print("No records found")