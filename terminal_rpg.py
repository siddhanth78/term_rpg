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
            'equipped':'rock'}

def display(board):
    board[player['row']][player['col']] = '#'
    for b in board:
        print(''.join(b))
    print('\n'+player['look'])
    print("Inventory\n")
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
        for i in range(len(b)):
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
                if ch == b'w': player['row'] -= 1
                elif ch == b'a': player['col'] -= 1
                elif ch == b's': player['row'] += 1
                elif ch == b'd': player['col'] += 1
                elif ch == b'\r': board = action(board)
                elif ch == b'1': player['equipped'] = player['inventory'][0]
                elif ch == b'2': player['equipped'] = player['inventory'][1]
                elif ch == b'3': player['equipped'] = player['inventory'][2]
                elif ch == b'4': player['equipped'] = player['inventory'][3]
                elif ch == b'5': player['equipped'] = player['inventory'][4]
                elif ch == b'6': player['equipped'] = player['inventory'][5]
            
                if player['row'] < 0: player['row'] = 0
                elif player['row'] > 9: player['row'] = 9
                
                if player['col'] < 0: player['col'] = 0
                elif player['col'] > 19: player['col'] = 19
            
            display(board)
    
main()