import msvcrt
import sys
import os
import random
import time
import string
import json

os.system("cls")

resources = ["stone", "wood", "steel", "iron", "diamond", "gold"]

boards = {}

mine = {}

mine_tiles = ["/", "-", "\\", "[", "]", "_"]

resource_icon = {
    "wood": "=",
    "stone": "*",
    "steel": "|",
    "iron": "+",
    "diamond": "^",
    "gold": "@",
}

player = {
    "row": 0,
    "col": 0,
    "board_n": 1,
    "mine_board_n": 1,
    "look": "right",
    "inventory": [
        "axe",
        "hammer",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
        "empty",
    ],
    "stone": 0,
    "wood": 0,
    "iron": 0,
    "steel": 0,
    "gold": 0,
    "diamond": 0,
    "axe": 1,
    "hammer": 1,
    "equipped": "axe",
}


def display(board):
    board[player["row"]][player["col"]] = "#"
    for b in board:
        print("".join(b))
    current_resources = [
        f"{item}: {player[item]}" for item in player["inventory"] if item != "empty"
    ]
    print("\n" + player["look"])
    print("Max inventory slots: 9")
    print("Inventory")
    print(" | ".join(current_resources))
    print("Equipped: " + player["equipped"])


def init_mine(n):
    board = [
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
    ]

    for b in board[1:9]:
        for i in range(1, len(b) - 1):
            prob = random.random()
            if 0.05 < prob <= (0.08 - n * 0.001):
                b[i] = "*"
            elif 0.08 < prob <= (0.1 - n * 0.001):
                b[i] = "+"
            elif 0.1 < prob <= (0.101 + n * 0.001):
                b[i] = "@"
            elif 0.25 < prob <= (0.2515 + n * 0.0005):
                b[i] = "^"

    board[-2][-2] = "]"
    board[-2][-3] = "_"
    board[-2][-4] = "["

    board[-3][-2] = "\\"
    board[-3][-3] = " "
    board[-3][-4] = "/"

    board[-4][-3] = "_"

    return board


def init_board():
    board = [
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
        ["."] * 20,
    ]

    for b in board[1:9]:
        for i in range(1, len(b) - 1):
            prob = random.random()
            if prob <= 0.08:
                b[i] = "T"
            elif 0.08 < prob <= 0.09:
                b[i] = "*"
            elif 0.09 < prob <= 0.095:
                b[i] = "+"
            elif 0.095 < prob <= 0.0965:
                b[i] = "@"
            elif 0.0975 < prob <= 0.09775:
                b[i] = "^"

    prob_mine = random.random()

    if prob_mine <= 0.03:
        board[-2][-2] = "]"
        board[-2][-3] = "_"
        board[-2][-4] = "["

        board[-3][-2] = "\\"
        board[-3][-3] = " "
        board[-3][-4] = "/"

        board[-4][-3] = "_"

    return board


def action(board):
    if player["look"] == "up" and player["row"] != 0:
        return check_state(board, player["row"] - 1, player["col"])
    elif player["look"] == "down" and player["row"] != 9:
        return check_state(board, player["row"] + 1, player["col"])
    elif player["look"] == "right" and player["col"] != 19:
        return check_state(board, player["row"], player["col"] + 1)
    elif player["look"] == "left" and player["col"] != 0:
        return check_state(board, player["row"], player["col"] - 1)


def check_state(board, row, col):
    if (
        player["equipped"] == "axe"
        and player["axe"] >= 1
        and board[row][col]
        in [
            "T",
            "=", 
        ]
    ):
        board[row][col] = "."
        player["wood"] += 1
        if "wood" not in player["inventory"]:
            player["inventory"][player["inventory"].index("empty")] = "wood"
    elif (
        player["equipped"] == "hammer"
        and player["hammer"] >= 1
        and board[row][col] == "*"
    ):
        board[row][col] = "."
        player["stone"] += 1
        if "stone" not in player["inventory"]:
            player["inventory"][player["inventory"].index("empty")] = "stone"
    elif player["equipped"] in resources:
        if board[row][col] == "." and player[player["equipped"]] > 0:
            board[row][col] = resource_icon[player["equipped"]]
            player[player["equipped"]] -= 1
            if player[player["equipped"]] == 0:
                player["inventory"][
                    player["inventory"].index(player["equipped"])
                ] = "empty"
                player["equipped"] = "empty"

    return board


def generate_world(n):
    grid_size = n * n
    progress_milestone = grid_size // 10
    progress = "[" + " " * 10 + "]"
    print(f"Generating world ({n}x{n})... {progress}")
    c = 0
    for i in range(1, grid_size + 1):
        boards[i] = init_board()
        if i % progress_milestone == 0:
            c += 1
            progress = "[" + "#" * c + " " * (10 - c) + "]"
            sys.stdout.write("\0338\033[0J")
            sys.stdout.flush()
            print(f"Generating world ({n}x{n})... {progress}")


def generate_mine():
    sys.stdout.write("\0338\033[0J")
    sys.stdout.flush()
    grid_size = random.randint(10, 31)
    progress_milestone = grid_size // 10
    progress = "[" + " " * 10 + "]"
    print(f"Generating mine ({grid_size} levels)... {progress}")
    c = 0
    for i in range(1, grid_size + 1): 
        mine[i] = init_mine(i)
        if i % progress_milestone == 0:
            c += 1
            progress = "[" + "#" * c + " " * (10 - c) + "]"
            sys.stdout.write("\0338\033[0J")
            sys.stdout.flush()
            print(f"Generating mine ({grid_size} levels)... {progress}")
    time.sleep(1)


def enter_mine(curr_area, board, temp_bn):
    if temp_bn != player["board_n"]:
        generate_mine()
    temp_bn = player["board_n"]
    player["mine_board_n"] = 1
    curr_area = mine
    board = curr_area[player["mine_board_n"]]
    in_mine = True
    return in_mine, curr_area, board, temp_bn


def exit_mine(curr_area, board, temp_bn):
    player["board_n"] = temp_bn
    curr_area = boards
    board = curr_area[player["board_n"]]
    in_mine = False
    return in_mine, curr_area, board
    
def load(w_id):
    with open(f"worlds/{w_id}.world", "r") as f:
        all_boards = f.read().split("\n%===%\n")
        all_boards.remove("")
        c = 1
        for ab in all_boards:
            rows = ab.split("\n")
            boards[c] = [list(row) for row in rows]
            c += 1
    with open(f"players/{w_id}.player", "r") as fp:
        player = json.loads(fp.read())
    return boards, player
            
def save(w_id):
    with open(f"worlds/{w_id}.world", "w") as f:
        for i in range(1, 250001):
            for b in boards[i]:
                row = ''.join(b)
                row += "\n"
                f.write(row)
            f.write("%===%\n")
    with open(f"players/{w_id}.player", "w") as fp:
        fp.write(json.dumps(player))

def start(w_id, boards, player):
    sys.stdout.write("\0338\033[0J")
    sys.stdout.flush()
    curr_area = boards
    player["row"] = 0
    player["col"] = 0
    print(f'Tile: {(player["board_n"]%500)-1}, {player["board_n"]//500}\n')
    board = curr_area[player["board_n"]]
    display(board)
    player["mine_board_n"] = 1
    in_mine = False
    w_id = w_id
    temp_bn = 0

    tiles = ["T", "*", "=", "@", "+", "^", "|", "/", "\\", "_", "[", "]", "-"]

    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            board[player["row"]][player["col"]] = "."

            if ch == b"\xe0":
                ch = msvcrt.getch()
                if ch == b"H":
                    player["look"] = "up"
                elif ch == b"P":
                    player["look"] = "down"
                elif ch == b"K":
                    player["look"] = "left"
                elif ch == b"M":
                    player["look"] = "right"

            elif ch == b"\x1b":
                sys.stdout.write("\0338\033[0J")
                sys.stdout.flush()
                print("Quitting...")
                print("Saving...")
                save(w_id)
                os.system("cls")
                sys.stdout.write("\0337")
                sys.stdout.write("\033[?25l")
                sys.stdout.flush()
                break

            elif ch == b"w":
                player["look"] = "up"
                if player["row"] - 1 < 0:
                    if in_mine == False:
                        if player["board_n"] > 500:
                            player["board_n"] -= 500
                            board = curr_area[player["board_n"]]
                            player["row"] = 9
                        else:
                            player["row"] = 0
                    else:
                        if player["mine_board_n"] > 1:
                            player["mine_board_n"] -= 1
                            board = curr_area[player["mine_board_n"]]
                            player["row"] = 9
                        else:
                            player["row"] = 0

                elif board[player["row"] - 1][player["col"]] not in tiles:
                    player["row"] -= 1

            elif ch == b"a":
                player["look"] = "left"
                if player["col"] - 1 < 0:
                    if in_mine == False:
                        if player["board_n"] % 500 != 1:
                            player["board_n"] -= 1
                            board = curr_area[player["board_n"]]
                            player["col"] = 19
                        else:
                            player["col"] = 0
                    else:
                        player["col"] = 0

                elif board[player["row"]][player["col"] - 1] not in tiles:
                    player["col"] -= 1

            elif ch == b"s":
                player["look"] = "down"
                if player["row"] + 1 > 9:
                    if in_mine == False:
                        if player["board_n"] < 249501:
                            player["board_n"] += 500
                            board = curr_area[player["board_n"]]
                            player["row"] = 0
                        else:
                            player["row"] = 9
                    else:
                        if player["mine_board_n"] < len(mine):
                            player["mine_board_n"] += 1
                            board = curr_area[player["mine_board_n"]]
                            player["row"] = 0
                        else:
                            player["row"] = 9

                elif board[player["row"] + 1][player["col"]] not in tiles:
                    player["row"] += 1

            elif ch == b"d":
                player["look"] = "right"
                if player["col"] + 1 > 19:
                    if in_mine == False:
                        if player["board_n"] % 500 != 0:
                            player["board_n"] += 1
                            board = curr_area[player["board_n"]]
                            player["col"] = 0
                        else:
                            player["col"] = 19
                    else:
                        player["col"] = 19

                elif board[player["row"]][player["col"] + 1] not in tiles:
                    player["col"] += 1

            elif ch == b"\r":
                if (
                    (
                        player["look"] == "up"
                        and (board[player["row"] - 1][player["col"]] in mine_tiles)
                    )
                    or (
                        player["look"] == "down"
                        and (board[player["row"] + 1][player["col"]] in mine_tiles)
                    )
                    or (
                        player["look"] == "left"
                        and (board[player["row"]][player["col"] - 1] in mine_tiles)
                    )
                    or (
                        player["look"] == "right"
                        and (board[player["row"]][player["col"] + 1] in mine_tiles)
                    )
                ):
                    if in_mine == False:
                        in_mine, curr_area, board, temp_bn = enter_mine(
                            curr_area, board, temp_bn
                        )
                    elif in_mine == True:
                        in_mine, curr_area, board = exit_mine(
                            curr_area, board, temp_bn
                        )
                else:
                    board = action(board)
            elif ch == b"1":
                player["equipped"] = player["inventory"][0]
            elif ch == b"2":
                player["equipped"] = player["inventory"][1]
            elif ch == b"3":
                player["equipped"] = player["inventory"][2]
            elif ch == b"4":
                player["equipped"] = player["inventory"][3]
            elif ch == b"5":
                player["equipped"] = player["inventory"][4]
            elif ch == b"6":
                player["equipped"] = player["inventory"][5]
            elif ch == b"7":
                player["equipped"] = player["inventory"][6]
            elif ch == b"8":
                player["equipped"] = player["inventory"][7]
            elif ch == b"9":
                player["equipped"] = player["inventory"][8]

            sys.stdout.write("\0338\033[0J")
            sys.stdout.flush()
            print(f'Tile: {(player["board_n"]%500)-1}, {player["board_n"]//500}\n')
            display(board)

if __name__ == "__main__":
    with open(".settings", "r") as f:
        settings = json.loads(f.read())
    while True:
        print(f'Max world slots: {settings["max_slots"]}')
        print("1. Load world")
        print("2. New world")
        print("3. Delete world")
        print("4. Show worlds")
        print("5. Set max world slots (Warning: each world takes up about 55 MB)")
        print("6. Exit")
        try:
            choice = int(input("Enter option: "))
        except:
            print("Invalid\n")
            continue
        else:
            print()
            if choice == 1:
                if settings["worlds_available"] == 0:
                    print("No worlds available to load\n")
                    continue
                w_id = input("Enter world ID: ")
                if os.path.exists(f"worlds/{w_id}.world"):
                    os.system("cls")
                    sys.stdout.write("\0337")
                    sys.stdout.write("\033[?25l")
                    sys.stdout.flush()
                    print(f"Loading world...")
                    boards, player = load(w_id)
                    with open(".settings", "w") as f:
                        f.write(json.dumps(settings))
                    start(w_id, boards, player)
                else:
                    print("World doesn't exist\n")
            elif choice == 2:
                if settings["worlds_available"] + 1 > settings["max_slots"]:
                    print("Max world slots exceeded\n")
                else:
                    os.system("cls")
                    sys.stdout.write("\0337")
                    sys.stdout.write("\033[?25l")
                    sys.stdout.flush()
                    sys.stdout.write("\0338\033[0J")
                    sys.stdout.flush()
                    generate_world(500)
                    w_id = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)), ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)),
                                    ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)), ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))])
                    print(f"World ID: {w_id}")
                    settings["worlds_available"] += 1
                    print("Saving...")
                    save(w_id)
                    settings["all_worlds"].append(w_id)
                    with open(".settings", "w") as f:
                        f.write(json.dumps(settings))
                    start(w_id, boards, player)
            elif choice == 3:
                if settings["worlds_available"] == 0:
                    print("No worlds available to delete\n")
                    continue
                w_id = input("Enter world ID: ")
                if os.path.exists(f"worlds/{w_id}.world"):
                    os.remove(f"worlds/{w_id}.world")
                    os.remove(f"players/{w_id}.player")
                    settings["worlds_available"] -= 1
                    settings["all_worlds"].remove(w_id)
                    print("World deleted\n")
                else:
                    print("World doesn't exist\n")
            elif choice == 4:
                print("World IDs:\n")
                for aw in settings["all_worlds"]:
                    print(aw)
                print()
            elif choice == 5:
                try:
                    settings["max_slots"] = int(input("Enter new max: "))
                except:
                    print("Invalid\n")
                else:
                    print(f'New max world slots: {settings["max_slots"]}\n')
            elif choice == 6:
                with open(".settings", "w") as f:
                    f.write(json.dumps(settings))
                quit()
            else:
                print("Invalid\n")