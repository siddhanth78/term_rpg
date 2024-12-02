import msvcrt
import sys
import os
import random

os.system("cls")

sys.stdout.write("\0337")
sys.stdout.write("\033[?25l")
sys.stdout.flush()

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
            if 0.05 < prob <= (0.07 - n*0.001):
                b[i] = "*"
            elif 0.07 < prob <= (0.08 - n*0.001):
                b[i] = "+"
            elif 0.08 < prob <= (0.085 + n*0.001):
                b[i] = "@"
            elif 0.09 < prob <= (0.091 + n*0.001):
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
            if prob <= 0.05:
                b[i] = "T"
            elif 0.05 < prob <= 0.06:
                b[i] = "*"
            elif 0.06 < prob <= 0.065:
                b[i] = "+"
            elif 0.065 < prob <= 0.0665:
                b[i] = "@"
            elif 0.0675 < prob <= 0.06775:
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
        if (
            player["equipped"] == "axe"
            and player["axe"] >= 1
            and board[player["row"] - 1][player["col"]]
            in [
                "T",
                "=",
            ]
        ):
            board[player["row"] - 1][player["col"]] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and player["hammer"] >= 1
            and board[player["row"] - 1][player["col"]] == "*"
        ):
            board[player["row"] - 1][player["col"]] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"

        elif player["equipped"] in resources:
            if (
                board[player["row"] - 1][player["col"]] == "."
                and player[player["equipped"]] > 0
            ):
                board[player["row"] - 1][player["col"]] = resource_icon[
                    player["equipped"]
                ]
                player[player["equipped"]] -= 1
                if player[player["equipped"]] == 0:
                    player["inventory"][
                        player["inventory"].index(player["equipped"])
                    ] = "empty"
                    player["equipped"] = "empty"

    elif player["look"] == "down" and player["row"] != 9:
        if (
            player["equipped"] == "axe"
            and player["axe"] >= 1
            and board[player["row"] + 1][player["col"]]
            in [
                "T",
                "=",
            ]
        ):
            board[player["row"] + 1][player["col"]] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and player["hammer"] >= 1
            and board[player["row"] + 1][player["col"]] == "*"
        ):
            board[player["row"] + 1][player["col"]] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif player["equipped"] in resources:
            if (
                board[player["row"] + 1][player["col"]] == "."
                and player[player["equipped"]] > 0
            ):
                board[player["row"] + 1][player["col"]] = resource_icon[
                    player["equipped"]
                ]
                player[player["equipped"]] -= 1
                if player[player["equipped"]] == 0:
                    player["inventory"][
                        player["inventory"].index(player["equipped"])
                    ] = "empty"
                    player["equipped"] = "empty"

    elif player["look"] == "right" and player["col"] != 19:
        if (
            player["equipped"] == "axe"
            and player["axe"] >= 1
            and board[player["row"]][player["col"] + 1]
            in [
                "T",
                "=",
            ]
        ):
            board[player["row"]][player["col"] + 1] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and player["hammer"] >= 1
            and board[player["row"]][player["col"] + 1] == "*"
        ):
            board[player["row"]][player["col"] + 1] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif player["equipped"] in resources:
            if (
                board[player["row"]][player["col"] + 1] == "."
                and player[player["equipped"]] > 0
            ):
                board[player["row"]][player["col"] + 1] = resource_icon[
                    player["equipped"]
                ]
                player[player["equipped"]] -= 1
                if player[player["equipped"]] == 0:
                    player["inventory"][
                        player["inventory"].index(player["equipped"])
                    ] = "empty"
                    player["equipped"] = "empty"

    elif player["look"] == "left" and player["col"] != 0:
        if (
            player["equipped"] == "axe"
            and player["axe"] >= 1
            and board[player["row"]][player["col"] - 1]
            in [
                "T",
                "=",
            ]
        ):
            board[player["row"]][player["col"] - 1] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and player["hammer"] >= 1
            and board[player["row"]][player["col"] - 1] == "*"
        ):
            board[player["row"]][player["col"] - 1] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif player["equipped"] in resources:
            if (
                board[player["row"]][player["col"] - 1] == "."
                and player[player["equipped"]] > 0
            ):
                board[player["row"]][player["col"] - 1] = resource_icon[
                    player["equipped"]
                ]
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
    for i in range(grid_size):
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
    for i in range(grid_size):
        mine[i] = init_mine(i)
        if i % progress_milestone == 0:
            c += 1
            progress = "[" + "#" * c + " " * (10 - c) + "]"
            sys.stdout.write("\0338\033[0J")
            sys.stdout.flush()
            print(f"Generating mine ({grid_size} levels)... {progress}")
    
def enter_mine(curr_area, board, board_n, curr_board_n):
    if curr_board_n != board_n:
        generate_mine()
    curr_board_n = board_n
    board_n = 0
    curr_area = mine
    board = curr_area[board_n]
    in_mine = True
    return in_mine, curr_area, board, board_n, curr_board_n

def exit_mine(curr_area, board, board_n, curr_board_n):
    board_n = curr_board_n
    curr_area = boards
    board = curr_area[board_n]
    in_mine = False
    return in_mine, curr_area, board, board_n

def start():
    sys.stdout.write("\0338\033[0J")
    sys.stdout.flush()
    board_n = 1
    curr_area = boards
    board = curr_area[board_n]
    print(f"Tile: {(board_n%500)-1}, {board_n//500}\n")
    display(board)
    curr_board_n = board_n
    in_mine = False

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

            elif ch == b"w":
                player["look"] = "up"
                if player["row"] - 1 < 0:
                    if in_mine == False:
                        if board_n > 500:
                            board_n -= 500
                            board = curr_area[board_n]
                            player["row"] = 9
                        else:
                            player["row"] = 0
                    else:
                        if board_n > 0:
                            board_n -= 1
                            board = curr_area[board_n]
                            player["row"] = 9
                        else:
                            player["row"] = 0
                            
                elif board[player["row"] - 1][player["col"]] not in tiles:
                    player["row"] -= 1

            elif ch == b"a":
                player["look"] = "left"
                if player["col"] - 1 < 0:
                    if in_mine == False:
                        if board_n % 500 != 1:
                            board_n -= 1
                            board = curr_area[board_n]
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
                        if board_n < 249501:
                            board_n += 500
                            board = curr_area[board_n]
                            player["row"] = 0
                        else:
                            player["row"] = 9
                    else:
                        if board_n < len(mine):
                            board_n += 1
                            board = curr_area[board_n]
                            player["row"] = 0
                        else:
                            player["row"] = 9
                            
                elif board[player["row"] + 1][player["col"]] not in tiles:
                    player["row"] += 1

            elif ch == b"d":
                player["look"] = "right"
                if player["col"] + 1 > 19:
                    if in_mine == False:
                        if board_n % 500 != 0:
                            board_n += 1
                            board = curr_area[board_n]
                            player["col"] = 0
                        else:
                            player["col"] = 19
                    else:
                        player["col"] = 19
                            
                elif board[player["row"]][player["col"] + 1] not in tiles:
                    player["col"] += 1

            elif ch == b"\r":
                if player["look"] == "up" and (board[player["row"] - 1][player["col"]] in mine_tiles):
                    if in_mine == False:
                        in_mine, curr_area, board, board_n, curr_board_n = enter_mine(curr_area, board, board_n, curr_board_n)
                    elif in_mine == True:
                        in_mine, curr_area, board, board_n = exit_mine(curr_area, board, board_n, curr_board_n)
                elif player["look"] == "down" and (board[player["row"] + 1][player["col"]] in mine_tiles):
                    if in_mine == False:
                        in_mine, curr_area, board, board_n, curr_board_n = enter_mine(curr_area, board, board_n, curr_board_n)
                    elif in_mine == True:
                        in_mine, curr_area, board, board_n = exit_mine(curr_area, board, board_n, curr_board_n)
                elif player["look"] == "left" and (board[player["row"]][player["col"] - 1] in mine_tiles):
                    if in_mine == False:
                        in_mine, curr_area, board, board_n, curr_board_n = enter_mine(curr_area, board, board_n, curr_board_n)
                    elif in_mine == True:
                        in_mine, curr_area, board, board_n = exit_mine(curr_area, board, board_n, curr_board_n)
                elif player["look"] == "right" and (board[player["row"]][player["col"] + 1] in mine_tiles):
                    if in_mine == False:
                        in_mine, curr_area, board, board_n, curr_board_n = enter_mine(curr_area, board, board_n, curr_board_n)
                    elif in_mine == True:
                        in_mine, curr_area, board, board_n = exit_mine(curr_area, board, board_n, curr_board_n)
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
            print(f"Tile: {(board_n%500)-1}, {board_n//500}\n")
            display(board)


generate_world(500)
start()
