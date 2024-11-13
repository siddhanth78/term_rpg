import msvcrt
import sys
import os
import keyboard
import random

os.system('cls')

sys.stdout.write('\0337')
sys.stdout.write('\033[?25l')
sys.stdout.flush()

player = {'row':0,
            'col':0,
            'look':'right',
            'inventory':['axe', 'sword', 'rock', 'empty', 'empty', 'empty'],
            'equipped':'axe'}

def display(board):
    board[player['row']][player['col']] = '#'
    for b in board:
        print(''.join(b))
    print('\n'+player['look'])
    print("\nInventory\n")
    for i in player['inventory']:
        if i == 'empty':
            print('[   ]')
            print('[   ]\n')
        elif i == 'rock':
            print('[   ]')
            print('[( )]\n')
        elif i == 'axe':
            print('[<|>]')
            print('[ | ]\n')
        elif i == 'sword':
            print('[ | ]')
            print('[ + ]\n')
    print('\n'+player['equipped'])
        
def init_board():
    board = [['.']*20,['.']*20,['.']*20,['.']*20,['.']*20,
            ['.']*20,['.']*20,['.']*20,['.']*20,['.']*20,]
            
    for b in board:
        for i in range(1,len(b)):
            prob = random.random()
            if prob <= 0.1:
                b[i] = 'T'
                
    return board
    
def action(board):
    if player['look'] == 'up' and player['row'] != 0:
        if player['equipped'] == 'axe' and board[player['row']-1][player['col']] == 'T':
            board[player['row']-1][player['col']] = '.'
    elif player['look'] == 'down' and player['row'] != 9:
        if player['equipped'] == 'axe' and board[player['row']+1][player['col']] == 'T':
            board[player['row']+1][player['col']] = '.'
    elif player['look'] == 'right' and player['col'] != 19:
        if player['equipped'] == 'axe' and board[player['row']][player['col']+1] == 'T':
            board[player['row']][player['col']+1] = '.'
    elif player['look'] == 'left' and player['col'] != 0:
        if player['equipped'] == 'axe' and board[player['row']][player['col']-1] == 'T':
            board[player['row']][player['col']-1] = '.'
    
    return board
        
def main():
    board = init_board()
    display(board)
    
    while True:
        if msvcrt.kbhit():
            sys.stdout.write('\0338\033[0J')
            sys.stdout.flush()
            
            ch = msvcrt.getch()
            board[player['row']][player['col']] = '.'
            
            if ch == b'\xe0':
                ch = msvcrt.getch()
                if ch == b'H':
                    player['look'] = 'up'
                elif ch == b'P':
                    player['look'] = "down"
                elif ch == b'K':
                    player['look'] = "left"
                elif ch == b'M':
                    player['look'] = "right"
            else:
                if ch == b'w' and player['row']-1 >= 0:
                    if board[player['row']-1][player['col']] != 'T': player['row'] -= 1
                elif ch == b'a' and player['col']-1 >= 0:
                    if board[player['row']][player['col']-1] != 'T': player['col'] -= 1
                elif ch == b's' and player['row']+1 <= 9:
                    if board[player['row']+1][player['col']] != 'T': player['row'] += 1
                elif ch == b'd' and player['col']+1 <= 19:
                    if board[player['row']][player['col']+1] != 'T': player['col'] += 1
                elif ch == b'\r': board = action(board)
                elif ch == b'1': player['equipped'] = player['inventory'][0]
                elif ch == b'2': player['equipped'] = player['inventory'][1]
                elif ch == b'3': player['equipped'] = player['inventory'][2]
                elif ch == b'4': player['equipped'] = player['inventory'][3]
                elif ch == b'5': player['equipped'] = player['inventory'][4]
                elif ch == b'6': player['equipped'] = player['inventory'][5]
            
            display(board)
    
main()