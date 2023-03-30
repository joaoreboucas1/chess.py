#!/usr/bin/env python3
# chess.py
# a study python program
# author: @joaoreboucas1, march 2023
import sys
from pathlib import Path

pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
colors = ['(b)', '(w)']
cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = [str(x) for x in range(1,9)]
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
    global knights_positions
    is_move_legal = False
    opposite_player = '(b)' if player == '(w)' else '(w)'
    to_square = move[-2:]
    to_col = to_square[0]
    to_row = int(to_square[1])
    pawn_direction = 1 if player=='(w)' else -1
    if len(move)==2:
        # Pawn move, like e4
        if (player=='(w)' and to_row==1) \
                or (player=='(b)' and to_row==8) \
                or board[to_square] != 'None':
            return None, to_square, is_move_legal

        from_col = to_col
        pawn_starting_row = 2 if player == '(w)' else 7
        if board[to_col+str(to_row - pawn_direction)] == 'P'+player:
            from_row = str(to_row - pawn_direction)
        elif to_row - 2*pawn_direction == pawn_starting_row \
                and board[to_col+str(to_row - 2*pawn_direction)] == 'P'+player \
                and board[to_col+str(to_row - pawn_direction)] == 'None':
            from_row = str(to_row - 2*pawn_direction)
        else:
            return None, to_square, is_move_legal
        is_move_legal = True
    
    if len(move) == 4 and move[0].islower():
        # Pawn capture, like dxe5
        from_col = move[0]
        from_row = str(to_row - pawn_direction)
        if board[to_square][-3:] != opposite_player \
                and board[from_square] == 'P'+player:
            return None, to_square, is_move_legal
        is_move_legal = True

    if len(move) == 3 and move[0] == 'B':
        # Bishop move, like Bf4
        dist_to_right_edge = ord('g') - ord(to_col)
        dist_to_top_edge = 8 - to_row
        dist_to_left_edge = ord(to_col) - ord('a')
        dist_to_bottom_edge = to_row - 1

        # Searching secondary diagonal
        found_piece_1 = False
        for i in range(-min(dist_to_left_edge, dist_to_top_edge), min(dist_to_right_edge, dist_to_bottom_edge) + 1):
            from_row = f'{to_row - i}'
            from_col = chr(ord(to_col) + i)
            from_square = from_col + from_row
            if board[from_square] != 'None' and board[from_square] != 'B'+player:
                if is_move_legal:
                    is_move_legal = False
            if board[from_square] == 'B'+player:
                bishop_square = from_square
                is_move_legal = (True != found_piece_1)
                   
        # Searching main diagonal
        found_piece_2 = False
        for i in range(-min(dist_to_left_edge, dist_to_bottom_edge), min(dist_to_right_edge, dist_to_top_edge) + 1):
            from_row = f'{to_row + i}'
            from_col = chr(ord(to_col) + i)
            from_square = from_col + from_row
            if board[from_square] != 'None' and board[from_square] != 'B'+player:
                if is_move_legal:
                    is_move_legal = False
            if board[from_square] == 'B'+player:
                bishop_square = from_square
                is_move_legal = (True != found_piece_2)
        return bishop_square, to_square, is_move_legal
    
    if len(move) == 3 and move[0] == 'N':
        # Knight move, like Nf3
        knights_available = []
        if board[to_square] != 'None':
            return None, to_square, is_move_legal
        for from_square in knights_positions[player]:
            from_col, from_row = from_square
            from_row = int(from_row)
            if (abs(to_row - from_row) == 1 and abs(ord(to_col) - ord(from_col)) == 2) or (abs(to_row - from_row) == 2 and abs(ord(to_col) - ord(from_col)) == 1):
                knights_available.append(True)
            else:
                knights_available.append(False)
        
        is_move_legal = knights_available[0] != knights_available[1]
        if is_move_legal:
            from_square = knights_positions[player][0] if knights_available[0] else knights_positions[player][1]
            if knights_available[0]:
                knights_positions[player][0] = to_square
            else:
                knights_positions[player][1] = to_square
        return from_square, to_square, is_move_legal
    
    if len(move) == 4 and move[0] == 'N':
        # Knight captures, like Nxc6
        knights_available = []
        if board[to_square][-3:] != opposite_player or move[1] != 'x':
            return None, to_square, is_move_legal
        for from_square in knights_positions[player]:
            from_col, from_row = from_square
            from_row = int(from_row)
            if (abs(to_row - from_row) == 1 and abs(ord(to_col) - ord(from_col)) == 2) or (abs(to_row - from_row) == 2 and abs(ord(to_col) - ord(from_col)) == 1):
                knights_available.append(True)
            else:
                knights_available.append(False)
        
        is_move_legal = knights_available[0] != knights_available[1]
        if is_move_legal:
            from_square = knights_positions[player][0] if knights_available[0] else knights_positions[player][1]
            if knights_available[0]:
                knights_positions[player][0] = to_square
            else:
                knights_positions[player][1] = to_square
        return from_square, to_square, is_move_legal

    
    from_square = from_col+from_row
    return from_square, to_square, is_move_legal


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
        
        from_square, to_square, is_move_legal = translate_move(board, player, move)
        while not is_move_legal:
            move = input('Illegal move. Please, input a legal move: ')
            from_square, to_square, is_move_legal = translate_move(board, player, move)

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