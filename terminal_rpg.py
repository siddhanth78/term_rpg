import msvcrt
import sys
import os
import random

os.system("cls")

sys.stdout.write("\0337")
sys.stdout.write("\033[?25l")
sys.stdout.flush()

resources = ["stone", "wood", "steel", "iron", "diamond", "gold"]

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
    ],
    "stone": 0,
    "wood": 0,
    "iron": 0,
    "steel": 0,
    "gold": 0,
    "diamond": 0,
    "equipped": "axe",
}


def display(board):
    board[player["row"]][player["col"]] = "#"
    for b in board:
        print("".join(b))
    current_resources = [
        f"{item}: {player[item]}" if item in resources else item
        for item in player["inventory"]
    ]
    print("\n" + player["look"])
    print("\nInventory\n")
    print(" | ".join(current_resources))
    print("\nEquipped: " + player["equipped"])


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

    for b in board:
        for i in range(1, len(b)):
            prob = random.random()
            if prob <= 0.05:
                b[i] = "T"
            elif 0.05 < prob <= 0.06:
                b[i] = "*"
            elif 0.06 < prob <= 0.065:
                b[i] = "+"
            elif 0.065 < prob <= 0.0665:
                b[i] = "@"
            elif 0.0675 < prob <= 0.0677:
                b[i] = "^"

    return board


def action(board):
    if player["look"] == "up" and player["row"] != 0:
        if player["equipped"] == "axe" and board[player["row"] - 1][player["col"]] in [
            "T",
            "=",
        ]:
            board[player["row"] - 1][player["col"]] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and board[player["row"] - 1][player["col"]] == "*"
        ):
            board[player["row"] - 1][player["col"]] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif (
            player["equipped"] == "stone"
            and board[player["row"] - 1][player["col"]] == "."
            and player["stone"] > 0
        ):
            board[player["row"] - 1][player["col"]] = "*"
            player["stone"] -= 1
            if player["stone"] == 0:
                player["inventory"][player["inventory"].index("stone")] = "empty"
                player["equipped"] = "empty"
        elif (
            player["equipped"] == "wood"
            and board[player["row"] - 1][player["col"]] == "."
            and player["wood"] > 0
        ):
            board[player["row"] - 1][player["col"]] = "="
            player["wood"] -= 1
            if player["wood"] == 0:
                player["inventory"][player["inventory"].index("wood")] = "empty"
                player["equipped"] = "empty"
    elif player["look"] == "down" and player["row"] != 9:
        if player["equipped"] == "axe" and board[player["row"] + 1][player["col"]] in [
            "T",
            "=",
        ]:
            board[player["row"] + 1][player["col"]] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and board[player["row"] + 1][player["col"]] == "*"
        ):
            board[player["row"] + 1][player["col"]] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif (
            player["equipped"] == "stone"
            and board[player["row"] + 1][player["col"]] == "."
            and player["stone"] > 0
        ):
            board[player["row"] + 1][player["col"]] = "*"
            player["stone"] -= 1
            if player["stone"] == 0:
                player["inventory"][player["inventory"].index("stone")] = "empty"
                player["equipped"] = "empty"
        elif (
            player["equipped"] == "wood"
            and board[player["row"] + 1][player["col"]] == "."
            and player["wood"] > 0
        ):
            board[player["row"] + 1][player["col"]] = "="
            player["wood"] -= 1
            if player["wood"] == 0:
                player["inventory"][player["inventory"].index("wood")] = "empty"
                player["equipped"] = "empty"
    elif player["look"] == "right" and player["col"] != 19:
        if player["equipped"] == "axe" and board[player["row"]][player["col"] + 1] in [
            "T",
            "=",
        ]:
            board[player["row"]][player["col"] + 1] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and board[player["row"]][player["col"] + 1] == "*"
        ):
            board[player["row"]][player["col"] + 1] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif (
            player["equipped"] == "stone"
            and board[player["row"]][player["col"] + 1] == "."
            and player["stone"] > 0
        ):
            board[player["row"]][player["col"] + 1] = "*"
            player["stone"] -= 1
            if player["stone"] == 0:
                player["inventory"][player["inventory"].index("stone")] = "empty"
                player["equipped"] = "empty"
        elif (
            player["equipped"] == "wood"
            and board[player["row"]][player["col"] + 1] == "."
            and player["wood"] > 0
        ):
            board[player["row"]][player["col"] + 1] = "="
            player["wood"] -= 1
            if player["wood"] == 0:
                player["inventory"][player["inventory"].index("wood")] = "empty"
                player["equipped"] = "empty"
    elif player["look"] == "left" and player["col"] != 0:
        if player["equipped"] == "axe" and board[player["row"]][player["col"] - 1] in [
            "T",
            "=",
        ]:
            board[player["row"]][player["col"] - 1] = "."
            player["wood"] += 1
            if "wood" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "wood"
        elif (
            player["equipped"] == "hammer"
            and board[player["row"]][player["col"] - 1] == "*"
        ):
            board[player["row"]][player["col"] - 1] = "."
            player["stone"] += 1
            if "stone" not in player["inventory"]:
                player["inventory"][player["inventory"].index("empty")] = "stone"
        elif (
            player["equipped"] == "stone"
            and board[player["row"]][player["col"] - 1] == "."
            and player["stone"] > 0
        ):
            board[player["row"]][player["col"] - 1] = "*"
            player["stone"] -= 1
            if player["stone"] == 0:
                player["inventory"][player["inventory"].index("stone")] = "empty"
                player["equipped"] = "empty"
        elif (
            player["equipped"] == "wood"
            and board[player["row"]][player["col"] - 1] == "."
            and player["wood"] > 0
        ):
            board[player["row"]][player["col"] - 1] = "="
            player["wood"] -= 1
            if player["wood"] == 0:
                player["inventory"][player["inventory"].index("wood")] = "empty"
                player["equipped"] = "empty"

    return board


def start():
    board = init_board()
    display(board)

    tiles = ["T", "*", "=", "@", "+", "^", "|"]

    while True:
        if msvcrt.kbhit():
            sys.stdout.write("\0338\033[0J")
            sys.stdout.flush()

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

            elif ch == b"w" and player["row"] - 1 >= 0:
                player["look"] = "up"
                if board[player["row"] - 1][player["col"]] not in tiles:
                    player["row"] -= 1
            elif ch == b"a" and player["col"] - 1 >= 0:
                player["look"] = "left"
                if board[player["row"]][player["col"] - 1] not in tiles:
                    player["col"] -= 1
            elif ch == b"s" and player["row"] + 1 <= 9:
                player["look"] = "down"
                if board[player["row"] + 1][player["col"]] not in tiles:
                    player["row"] += 1
            elif ch == b"d" and player["col"] + 1 <= 19:
                player["look"] = "right"
                if board[player["row"]][player["col"] + 1] not in tiles:
                    player["col"] += 1
            elif ch == b"\r":
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

            display(board)


start()
