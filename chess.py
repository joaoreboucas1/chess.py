#!/usr/bin/env python3
# chess.py
# a study python program
# author: @joaoreboucas1, march 2023

pieces = ['P', 'R', 'N', 'B', 'Q', 'K']
colors=['(b)', '(w)']
cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows = [str(x) for x in range(1,9)]

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
    is_move_legal = False
    if player=='(w)':
        sign = 1
    else:
        sign = -1
    to_square = move[-2:]
    to_col = to_square[0]
    to_row = int(to_square[1])

    if len(move)==2:
        # Pawn move
        if (player=='(w)' and to_row==1) \
                or (player=='(b)' and to_row==8) \
                or board[to_square] != 'None':
            return to_square, to_square, is_move_legal

        from_col = to_col
        if board[to_col+str(to_row - sign)][0] == 'P':
            from_row = str(to_row - sign)
        elif board[to_col+str(to_row - 2*sign)][0] == 'P' and board[to_col+str(to_row - sign)] == 'None':
            from_row = str(to_row - 2*sign)
        else:
            return to_square, to_square, is_move_legal
        is_move_legal = True
    from_square = from_col+from_row
    return from_square, to_square, is_move_legal

class Chess:
    '''
    Description: a chess game.

    Attibutes:

    Methods:
    '''
    board = initialize_board()
    def __init__(self):
        pass

    def __str__(self):
        pass




if __name__=='__main__':
    print('chess.py')
    print('Starting game!')
    playing = True
    player = '(w)'
    board = initialize_board()
    print_board(board)
    while playing:
        move = input('{} to move: '.format(player))
        if move == 'q':
            break
        
        from_square, to_square, is_move_legal = translate_move(board, player, move)
        while not is_move_legal:
            move = input('Illegal move. Please, input a legal move: ')
            from_square, to_square, is_move_legal = translate_move(board, player, move)


        print('Moving {} from {} to {}'.format(board[from_square], from_square, to_square))
        move_piece(board, from_square, to_square)
        print_board(board)
        
        if player=='(w)':
            player = '(b)'
        elif player=='(b)':
            player = '(w)'