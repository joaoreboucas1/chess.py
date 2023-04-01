#!/usr/bin/env python3
# chess.py
# a study python program
# author: @joaoreboucas1, march 2023
import sys
from pathlib import Path
from math import copysign

pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
colors = ['(b)', '(w)']
cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = [str(x) for x in range(1,9)]
piece_locations = {'(w)':
                        {'P': ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
                        'R': ['a1', 'h1'],
                        'N': ['b1', 'g1'],
                        'B': ['c1', 'f1'],
                        'Q': 'd1',
                        'K': 'e1'},
                    '(b)':
                        {'P': ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
                        'R': ['a8', 'h8'],
                        'N': ['b8', 'g8'],
                        'B': ['c8', 'f8'],
                        'Q': 'd8',
                        'K': 'e8'}                        
                }
knights_positions = {'(w)': ['b1', 'g1'], '(b)': ['b8', 'g8']}

def initialize_board():
    '''
    Description: returns a `board` instance.

    Arguments:
        board: a dictionary whose keys are the board square names
    '''
    global cols, rows

    board = {}
    for col in cols:
        for row in rows:
            board[col+row] = 'None'

    for col in cols:
        board[col+'2'] = 'P(w)'
        board[col+'7'] = 'P(b)'
    
    board['a1'] = 'R(w)'
    board['b1'] = 'N(w)'
    board['c1'] = 'B(w)'
    board['d1'] = 'Q(w)'
    board['e1'] = 'K(w)'
    board['f1'] = 'B(w)'
    board['g1'] = 'N(w)'
    board['h1'] = 'R(w)'

    board['a8'] = 'R(b)'
    board['b8'] = 'N(b)'
    board['c8'] = 'B(b)'
    board['d8'] = 'Q(b)'
    board['e8'] = 'K(b)'
    board['f8'] = 'B(b)'
    board['g8'] = 'N(b)'
    board['h8'] = 'R(b)'
    return board


def print_board(board):
    for row in rows[::-1]:
        print(row, end='  ')
        for col in cols:
            print(board[col+row], end=' ')
        print()
    print('  ', end='')
    for col in cols:
        print('  ' + col +'  ', end='')
    print('')
    print('-'*(5*8 + 4))


def move_piece(board, from_square, to_square):
    '''
    Description: moves a piece from a square to another.
    '''
    board[to_square] = board[from_square]
    board[from_square] = 'None'


def translate_move(board, player, move):
    '''
    Translates a move in algebraic notation to a from_square and to_square
    '''
    global piece_locations
    error_msg = None
    is_move_legal = False
    opposite_player = '(b)' if player == '(w)' else '(w)'
    to_square = move[-2:]
    to_col = to_square[0]
    to_row = int(to_square[1])
    pawn_direction = 1 if player=='(w)' else -1
    if len(move)==2:
        # Pawn move, like e4
        if (player=='(w)' and to_row==1) or (player=='(b)' and to_row==8):
            error_msg = f'As {player}, {move} is an illegal move.'
            return None, to_square, is_move_legal, error_msg
        if board[to_square] != 'None':
            error_msg = f'The {to_square} square is occupied.'
            return None, to_square, is_move_legal, error_msg

        from_col = to_col
        pawn_starting_row = 2 if player == '(w)' else 7
        if board[to_col+str(to_row - pawn_direction)] == 'P'+player:
            from_row = str(to_row - pawn_direction)
        elif to_row - 2*pawn_direction == pawn_starting_row \
                and board[to_col+str(to_row - 2*pawn_direction)] == 'P'+player \
                and board[to_col+str(to_row - pawn_direction)] == 'None':
            from_row = str(to_row - 2*pawn_direction)
        else:
            error_msg = f'There is no pawn available to move to {move}.'
            return None, to_square, is_move_legal, error_msg
        is_move_legal = True
        from_square = from_col+from_row
        return from_square, to_square, is_move_legal, error_msg
    
    elif len(move) == 4 and move[0].islower():
        # Pawn capture, like dxe5
        from_col = move[0]
        from_row = str(to_row - pawn_direction)
        if board[to_square][-3:] != opposite_player \
                and board[from_square] == 'P'+player:
            error_msg = f'Pawn in {from_square} cannot capture {board[to_square]} in {to_square}.'
            return None, to_square, is_move_legal, error_msg
        is_move_legal = True
        from_square = from_col+from_row
        return from_square, to_square, is_move_legal, error_msg

    elif len(move) == 3 and move[0] == 'B':
        # Bishop move, like Bf4
        bishop_positions = piece_locations[player]['B']
        for i, bishop_position in enumerate(bishop_positions):
            if to_square == bishop_position:
                error_msg = 'Bishop is already in {to_square}.'
                return None, to_square, is_move_legal, error_msg

            to_col, to_row = to_square
            from_col, from_row = bishop_position
            horizontal_dist = ord(to_col) - ord(from_col)
            vertical_dist = int(to_row) - int(from_row)
            are_they_diagonally_connected = abs(horizontal_dist) == abs(vertical_dist)
            if are_they_diagonally_connected:
                if abs(vertical_dist) == 1:
                    is_move_legal = True
                    from_square = bishop_position
                    piece_locations[player]['B'][i] = to_square
                    return from_square, to_square, is_move_legal, error_msg
                else:
                    for j in range(1, abs(vertical_dist)):
                        sign_vertical = int(copysign(1, vertical_dist))
                        sign_horizontal = int(copysign(1, horizontal_dist))
                        trying_row = str(int(from_row) + j*sign_vertical)
                        trying_col = chr(ord(from_col) + j*sign_horizontal)
                        trying_square = trying_col + str(trying_row)
                        if board[trying_square] != 'None':
                            error_msg = f'Bishop in {bishop_position} cannot move to {to_square} because {board[trying_square]} in {trying_square} blocks the path.'
                            return None, to_square, is_move_legal, error_msg
                    is_move_legal = True
                    from_square = bishop_position
                    piece_locations[player]['B'][i] = to_square
                    return from_square, to_square, is_move_legal, error_msg
        
        error_msg = f'No bishop can move to {to_square}.'
        return None, to_square, is_move_legal, error_msg 
    
    elif len(move) == 3 and move[0] == 'N':
        # Knight move, like Nf3
        knights_positions = piece_locations[player]['N']
        knights_available = []
        if board[to_square] != 'None':
            error_msg = f'The {to_square} square is not empty, did you mean {move[0] + "x" + move[1:]}?'
            return None, to_square, is_move_legal, error_msg
        for from_square in knights_positions:
            from_col, from_row = from_square
            from_row = int(from_row)
            if (abs(to_row - from_row) == 1 and abs(ord(to_col) - ord(from_col)) == 2) or (abs(to_row - from_row) == 2 and abs(ord(to_col) - ord(from_col)) == 1):
                knights_available.append(True)
            else:
                knights_available.append(False)
        
        is_move_legal = knights_available[0] != knights_available[1]
        if is_move_legal:
            from_square = knights_positions[0] if knights_available[0] else knights_positions[1]
            if knights_available[0]:
                piece_locations[player]['N'][0] = to_square
            else:
                piece_locations[player]['N'][0] = to_square
        else:
            if knights_available[0]:
                error_msg = f'The move {move} is ambiguous: both knights in {knights_positions[0]} and {knights_positions[1]} can move to {to_square}.'
            else:
                error_msg = f'No knights can move to {to_square}.'
        return from_square, to_square, is_move_legal, error_msg
    
    elif len(move) == 4 and move[0] == 'N':
        # Knight captures, like Nxc6
        knights_positions = piece_locations[player]['N']
        knights_available = []
        if move[1] != 'x':
            error_msg = f'Invalid move: {move}'
            return None, to_square, is_move_legal, error_msg
        for from_square in knights_positions:
            from_col, from_row = from_square
            from_row = int(from_row)
            if (abs(to_row - from_row) == 1 and abs(ord(to_col) - ord(from_col)) == 2) or (abs(to_row - from_row) == 2 and abs(ord(to_col) - ord(from_col)) == 1):
                knights_available.append(True)
            else:
                knights_available.append(False)
        
        is_move_legal = knights_available[0] != knights_available[1]
        if is_move_legal:
            from_square = knights_positions[0] if knights_available[0] else knights_positions[1]
            if knights_available[0]:
                piece_locations[player]['N'][0] = to_square
            else:
                piece_locations[player]['N'][0] = to_square
        else:
            if knights_available[0]:
                error_msg = f'The move {move} is ambiguous: both knights in {knights_positions[0]} and {knights_positions[1]} can capture {board[to_square]} in {to_square}.'
        return from_square, to_square, is_move_legal, error_msg
    
    else:
        error_msg = f'Unrecognized move {move}.'
        return from_square, to_square, is_move_legal, error_msg


def play():
    '''
    Starts a chess.py match.
    '''
    print('chess.py starting game!')
    playing = True
    player = '(w)'
    board = initialize_board()
    print_board(board)
    while playing:
        move = input('{} to move: '.format('White' if player=='(w)' else 'Black'))
        if move == 'q':
            break
        
        from_square, to_square, is_move_legal, error_msg = translate_move(board, player, move)
        while not is_move_legal:
            move = input(f'{error_msg} Please, input a legal move: ')
            from_square, to_square, is_move_legal, error_msg = translate_move(board, player, move)

        if board[to_square] != 'None':
            print(f'{board[from_square]} captures {board[to_square]} on {to_square}')
        else:
            print(f'Moving {board[from_square]} from {from_square} to {to_square}')
        move_piece(board, from_square, to_square)
        print_board(board)
        
        if player=='(w)':
            player = '(b)'
        elif player=='(b)':
            player = '(w)'

def help():
    '''
    Explains algebraic notation
    '''
    with open('help.txt') as f:
        print(f.read())
    exit()

if __name__=='__main__':
    if len(sys.argv) == 1:
        program = Path(sys.argv[0]).name
        print(f'Usage: python {program} command')
        print('Available commands:')
        print('    play: start a game')
        print('    help: explain algebraic notation')
        exit()
    
    if sys.argv[1] == 'play':
        play()
        exit()

    if sys.argv[1] == 'help':
        help()
        exit()