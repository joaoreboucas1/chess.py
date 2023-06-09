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
piece_locations = {
    '(w)': {
        'P': ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
        'R': ['a1', 'h1'],
        'N': ['b1', 'g1'],
        'B': ['c1', 'f1'],
        'Q': ['d1'],
        'K': ['e1']
    },
    '(b)': {
        'P': ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
        'R': ['a8', 'h8'],
        'N': ['b8', 'g8'],
        'B': ['c8', 'f8'],
        'Q': ['d8'],
        'K': ['e8']
    }
}


def initialize_board():
    '''
    Description: returns a `board` instance.

    Arguments:
        board: a dictionary whose keys are the board square names
    '''
    global rows, cols
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
    global rows, cols
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


def process_bishop_move(board, player, move, is_queen=False):
    # Bishop move, like Bf4
    global rows, cols, piece_locations
    is_move_legal = False
    error_msg = None
    opposite_player = '(b)' if player == '(w)' else '(w)'

    # Recognize target square
    to_square = move[-2:]
    
    # Can some bishop move to the target square?
    # Conditions:
    # - the bishop square and the target square must be connected by a diagonal
    # - moving diagonally == moving the same distance vertically and horizontally
    # - if the squares are diagonally connected, there must be no pieces between them
    piece = 'B' if not is_queen else 'Q'
    bishop_positions = piece_locations[player][piece]
    for i, bishop_position in enumerate(bishop_positions):
        # Check the trivial case in which the bishop is already in the target square
        if to_square == bishop_position:
            error_msg = f'Bishop is already in {to_square}.'
            return None, to_square, is_move_legal, error_msg

        to_col, to_row = to_square
        from_col, from_row = bishop_position
        horizontal_dist = ord(to_col) - ord(from_col)
        vertical_dist = int(to_row) - int(from_row)
        are_squares_diagonally_connected = abs(horizontal_dist) == abs(vertical_dist)
        if are_squares_diagonally_connected:
            break
    
    if not are_squares_diagonally_connected:
        error_msg = f'No bishop can move to {move}.'
        return None, None, is_move_legal, error_msg

    # If the squares are diagonally connected, we need to check if there is a piece in the way
    if abs(vertical_dist) > 1:
        for j in range(1, abs(vertical_dist)):
            sign_vertical = int(vertical_dist/abs(vertical_dist))
            sign_horizontal = int(horizontal_dist/abs(horizontal_dist))
            trying_row = str(int(from_row) + j*sign_vertical)
            trying_col = chr(ord(from_col) + j*sign_horizontal)
            trying_square = trying_col + str(trying_row)
            if board[trying_square] != 'None':
                error_msg = f'Bishop in {bishop_position} cannot move to {to_square} because {board[trying_square]} in {trying_square} blocks the path.'
                return None, to_square, is_move_legal, error_msg

    is_move_legal = True
    from_square = bishop_position
    return from_square, to_square, is_move_legal, error_msg


def process_pawn_move(board, player, move):
    global rows, cols, piece_locations
    error_msg = None
    is_move_legal = False
    opposite_player = '(b)' if player == '(w)' else '(w)'

    # Recognize target square
    to_square = move[-2:]
    to_col = to_square[0]
    to_row = int(to_square[1])
    # Pawns move downward for black, upwards for white
    pawn_direction = 1 if player=='(w)' else -1

    # Pawn cannot move to the first (last) row if they are from white (black)
    if (player=='(w)' and to_row==1) or (player=='(b)' and to_row==8):
        error_msg = f'As {player}, {move} is an illegal move.'
        return None, to_square, is_move_legal, error_msg
    
    # Can a pawn move to the target square?
    # they can only move one square up (down)
    # if they are in their starting squares, they can move either one or two squares
    pawn_starting_row = 2 if player == '(w)' else 7
    if len(move) == 2 and (board[to_col + str(to_row - pawn_direction)] != 'P'+player \
            and (board[to_col + str(to_row - 2*pawn_direction)] != 'P'+player) and (to_row - 2*pawn_direction)==pawn_starting_row):
        error_msg = f'No pawn can move to {to_square}.'
        return None, None, is_move_legal, error_msg

    if len(move) == 2:
        from_row = (to_row - pawn_direction) if board[to_col+str(to_row - pawn_direction)] == 'P'+player else (to_row - 2*pawn_direction)
        from_square = to_col+str(from_row)
        is_move_legal = True

    # Can a pawn capture on the target square?
    if len(move) == 4:
        from_col = move[0]
        from_row = str(to_row - pawn_direction)
        from_square = from_col+from_row
        if board[from_square] != 'P'+player:
            error_msg = f'No pawn can capture in {to_square}.'
            return None, None, is_move_legal, error_msg
        is_move_legal = True
        # Update piece locations
        for i, pawn_location in enumerate(piece_locations[player]['P']):
            if pawn_location == from_square:
                piece_locations[player]['P'][i] = to_square
        captured_piece = board[to_square][0]
        for i, piece_location in enumerate(piece_locations[opposite_player][captured_piece]):
            if board[to_square] == piece_location:
                piece_locations[opposite_player][captured_piece][i] = 'Captured'
    return from_square, to_square, is_move_legal, error_msg


def process_pawn_captures(board, player, move):
    global rows, cols, piece_locations
    error_msg = None
    is_move_legal = False

    # Recognize target square
    to_square = move[-2:]
    to_row = int(to_square[1])
    to_col = to_square[0]
    # Pawns move downward for black, upwards for white
    pawn_direction = 1 if player=='(w)' else -1
    from_col = move[0]
    if abs(ord(from_col)-ord(to_col)) != 1:
        error_msg = f'Pawn in {from_col} cannot capture in {to_col}.'
        return None, None, is_move_legal, error_msg
    from_row = str(to_row - pawn_direction)
    from_square = from_col+from_row
    if board[from_square] != 'P'+player:
        error_msg = f'No pawn can capture in {to_square}.'
        return None, None, is_move_legal, error_msg
    is_move_legal = True
    return from_square, to_square, is_move_legal, error_msg


def process_knight_move(board, player, move):
    # Knight move, like Nf3
    global rows, cols, piece_locations
    error_msg = None
    is_move_legal = False
    opposite_player = '(b)' if player == '(w)' else '(w)'

    # Recognize target square
    to_square = move[-2:]
    to_col = to_square[0]
    to_row = int(to_square[1])

    knights_positions = piece_locations[player]['N']
    knights_available = []

    for from_square in knights_positions:
        from_col, from_row = from_square
        from_row = int(from_row)
        if (abs(to_row - from_row) == 1 and abs(ord(to_col) - ord(from_col)) == 2) or \
                (abs(to_row - from_row) == 2 and abs(ord(to_col) - ord(from_col)) == 1):
            knights_available.append(True)
        else:
            knights_available.append(False)
    
    is_move_legal = knights_available[0] != knights_available[1]
    if is_move_legal:      
        from_square = knights_positions[0] if knights_available[0] else knights_positions[1]
    else:
        if knights_available[0]:
            error_msg = f'The move {move} is ambiguous: both knights in {knights_positions[0]} and {knights_positions[1]} can move to {to_square}.'
        else:
            error_msg = f'No knights can move to {to_square}.'
        return None, None, is_move_legal, error_msg
    
    return from_square, to_square, is_move_legal, error_msg


def process_rook_move(board, player, move, is_queen=False):
    # Knight move, like Nf3
    global rows, cols, piece_locations
    error_msg = None
    is_move_legal = False
    opposite_player = '(b)' if player == '(w)' else '(w)'

    # Recognize target square
    to_square = move[-2:]
    to_col = to_square[0]
    to_row = to_square[1]

    piece = 'R' if not is_queen else 'Q'

    rook_locations = piece_locations[player][piece]
    available_rooks = []
    for rook_location in rook_locations:
        from_col, from_row = rook_location
        are_squares_vertically_connected = from_col == to_col
        vert_collision = False
        hor_collision = False
        if are_squares_vertically_connected:
            # Check for collision
            for i in range(1, abs(int(to_row) - int(from_row))):
                sign = -1 if (int(to_row) > int(from_row)) else 1
                mid_row = str(int(to_row) + i*sign)
                if board[to_col + mid_row] != 'None':
                    vert_collision = True
                    break
        are_squares_horizontally_connected = from_row == to_row
        if are_squares_horizontally_connected:
            # Check for collision
            for i in range(1, abs(ord(to_col) - ord(from_col))):
                sign = -1 if (ord(to_col) > ord(from_col)) else 1
                mid_col = chr(ord(to_col) + i*sign)
                print(mid_col)
                if board[mid_col + to_row] != 'None':
                    hor_collision = True
                    break
        if (are_squares_horizontally_connected and not hor_collision) or (are_squares_vertically_connected and not vert_collision):
            available_rooks.append(True)
        else:
            available_rooks.append(False)
    try:
        is_move_legal = available_rooks[0] != available_rooks[1]
    except:
        is_move_legal = available_rooks[0]
    if is_move_legal:        
        from_square = rook_locations[0] if rook_locations[0] else rook_locations[1]
    else:
        if available_rooks[0]:
            error_msg = f'The move {move} is ambiguous: both rooks in {rook_locations[0]} and {rook_locations[1]} can move to {to_square}.'
        else:
            error_msg = f'No rooks can move to {to_square}.'
        return None, None, is_move_legal, error_msg
    return from_square, to_square, is_move_legal, error_msg


def process_queen_move(board, player, move):  
    fictitious_move = 'B'+move[1:]
    from_square, to_square, is_move_legal, error_msg = process_bishop_move(board, player, fictitious_move, is_queen=True)
    if is_move_legal:
        return from_square, to_square, is_move_legal, error_msg

    fictitious_move = 'R'+move[1:]
    from_square, to_square, is_move_legal, error_msg = process_rook_move(board, player, fictitious_move, is_queen=True)
    if is_move_legal:
        return from_square, to_square, is_move_legal, error_msg
    
    return None, None, is_move_legal, error_msg


def process_king_move(board, player, move):
    global píece_locations, cols, rows
    is_move_legal = False
    error_msg = None
    opposite_player = '(b)' if player == '(w)' else '(w)'

    from_square = piece_locations[player]['K'][0]
    to_square = move[-2:]
    to_col, to_row = to_square
    from_col, from_row = from_square

    horizontal_dist = ord(to_col) - ord(from_col)
    vertical_dist = int(to_row) - int(from_row)

    is_move_legal = abs(horizontal_dist) <= 1 and abs(vertical_dist) <= 1

    return from_square, to_square, is_move_legal, error_msg


def process_long_castles(board, player, move):
    error_msg = None
    king_row = '1' if player=='(w)' else '8'
    opposite_player = '(b)' if player=='(w)' else '(w)'
    is_move_legal = board[f'e{king_row}']==f'K{player}' \
        and board[f'a{king_row}']==f'R{player}' \
        and (not is_square_threatened(board, opposite_player, f'b{king_row}')) \
        and (not is_square_threatened(board, opposite_player, f'c{king_row}')) \
        and (not is_square_threatened(board, opposite_player, f'd{king_row}'))
    if not is_move_legal:
        error_msg = "Cannot short castles because there are pieces in the way."
    return None, None, is_move_legal, error_msg


def process_short_castles(board, player, move):
    error_msg = None
    king_row = '1' if player=='(w)' else '8'
    opposite_player = '(b)' if player=='(w)' else '(w)'
    is_move_legal = board[f'e{king_row}']==f'K{player}' \
        and board[f'h{king_row}']==f'R{player}' \
        and (not is_square_threatened(board, opposite_player, f'f{king_row}')) \
        and (not is_square_threatened(board, opposite_player, f'g{king_row}'))
    if not is_move_legal:
        error_msg = "Cannot short castles because there are pieces in the way."
    return None, None, is_move_legal, error_msg


def is_square_threatened(board, player, square):
    '''
    Checks if `square` is threatened by `player`
    '''
    global pieces, piece_locations
    piece_processes = {
        'R': process_rook_move,
        'N': process_knight_move,
        'B': process_bishop_move,
        'Q': process_queen_move,
        'K': process_king_move,
        'P': process_pawn_captures
    }
    for piece in pieces:
        specific_piece_locations = piece_locations[player][piece]
        if specific_piece_locations is None:
            continue
        
        for location in specific_piece_locations:
            if piece == "P":
                pawn_col = location[0]
                move = f'{pawn_col}x{square}'
                _,_, is_move_legal,_ = piece_processes[piece](board, player, move)
            else:
                move = f'{piece}{square}' 
                _,_, is_move_legal,_ = piece_processes[piece](board, player, move)
            if is_move_legal:
                print(f"Piece {piece} from {player} in {location} is threatening {square}")
                return True
        return False


def process_move(board, player, move):
    '''
    Checks if move is a readable move. Then, checks if move is valid (i.e. the piece can move to the square)
    Translates a move in algebraic notation to a from_square and to_square
    '''
    global rows, cols, piece_locations
    error_msg = None
    is_move_legal = False
    opposite_player = '(b)' if player == '(w)' else '(w)'
    if move not in ['o-o', 'o-o-o']:
        to_square = move[-2:]
        to_col = to_square[0]
        to_row = int(to_square[1])
    pawn_direction = 1 if player=='(w)' else -1

    # Is the move readable?
    # In order for a move to be readable, it must:
    # - start with a piece name (N, B, R, K, Q) or a column name (pawn moves) or 'o' (castles)
    # - in case of piece moves, they must have 3, 4, or 5 chars
    #   - if they have 3 chars, then the last two chars must be a recognizable square on the board
    #   - if they have 4 chars, then the second char must be either a row, a col or 'x' and the last two chars must be a recognizable square on the board
    #   - if they have 5 chars, then the second char must be either a row, a col or 'x'; the third char must be 'x' and the last two chars must ber a recognizable square on the board
    # - in case of pawn moves, they must have 2 or 4 chars
    #   - if they have 2 chars, then the last two chars must be a recognizable square on the board
    #   - if they have 4 chars, then the second char must be 'x' and the last two chars must be a recognizable square on the board
    # - in case of castles, the moves are 'o-o' and 'o-o-o'
    if move[0] not in pieces + cols + ['o']:
        error_msg =  f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg
    
    if (move[0]=='o' and move not in ['o-o', 'o-o-o']) or move[-2:] not in board.keys():
        error_msg =  f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg

    if move[0] in pieces and len(move) not in [3,4,5]:
        error_msg =  f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg

    if move[0] in pieces and len(move) == 4 and move[1] not in rows + cols + ['x']:
        error_msg = f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg
    
    if move[0] in pieces and len(move) == 5 and (move[1] != 'x' or move[2] not in rows + cols + ['x']):
        error_msg = f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg
    
    if move[0] in cols and len(move) not in [2,4]:
        error_msg =  f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg

    if move[0] in cols and len(move) == 4 and move[1] != 'x':
        error_msg = f'Unrecognizable move: {move}.'
        return None, None, is_move_legal, error_msg

    # Processing moves
    if move[0] in cols:
        if len(move) == 2:
            return process_pawn_move(board, player, move)
        else:
            return process_pawn_captures(board, player, move)
    
    elif move[0] == 'B':
        return process_bishop_move(board, player, move)
    
    elif move[0] == 'N':
        return process_knight_move(board, player, move)

    elif move[0] == 'R':
        return process_rook_move(board, player, move)
    
    elif move[0] == 'K':
        return process_king_move(board, player, move)
    
    elif move[0] == 'Q':
        return process_queen_move(board, player, move)

    elif move == 'o-o':
        # Short castles
        if player=='(w)':
            if board['e1'] != 'K'+player:
                error_msg = f"White's king must be on e1 to castle."
                return None, to_square, is_move_legal, error_msg
            if board['h1'] != 'R'+player:
                error_msg = f"White's rook must be on h1 to castle."
                return None, to_square, is_move_legal, error_msg
            if board['f1'] != 'None' or board['g1'] != 'None':
                if board['f1'] != 'None':
                    error_msg = f'Cannot short castles because {board["f1"]} in f1 blocks the path.'
                    return None, to_square, is_move_legal, error_msg
                else:
                    error_msg = f'Cannot short castles because {board["g1"]} in g1 blocks the path.'
                    return None, to_square, is_move_legal, error_msg
            is_move_legal = True
            board['f1'] = 'R'+player
            board['g1'] = 'K'+player
            board['e1'] = 'None'
            board['h1'] = 'None'
            return None, None, is_move_legal, error_msg 


    elif move == 'o-o-o':
        return process_long_castles(board, player, move)

    else:
        error_msg = f'Unrecognized move {move}.'
        return None, None, is_move_legal, error_msg


def check_validity(board, player, move):
    """
    Given a legal move, see which piece is in the landing square
    """
    from_square, to_square, is_move_legal, error_msg = process_move(board, player, move)
    
    if not is_move_legal:
        return None, None, is_move_legal, error_msg
    
    opposite_player = '(b)' if player=='(w)' else '(w)'
    if board[to_square][-3:] == player:
        return False, f"Cannot move {board[from_square]} to {to_square} because it's occupied by {board[to_square]}."
    
    if board[to_square][-3:] == opposite_player and (move[1] != 'x' or move[2] != 'x'):
        return False, f"""Cannot move {board[from_square]} to {to_square} because it's occupied by {board[to_square]}.
            Did you mean {move[0]}x{move[-2:]}?"""
    
    if board[to_square] == "None" and (move[1] == 'x' or (len(move) > 2 and move[2] == 'x')):
        return False, f"""Cannot capture on {to_square} because it's empty.
            Did you mean {move[0]}{move[-2:]}?"""
    
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
        from_square, to_square, is_move_legal, error_msg = check_validity(board, player, move)
        while not is_move_legal:
            move = input(f'{error_msg} Please, input a legal move: ')
            if move == 'q':
                exit()
            from_square, to_square, is_move_legal, error_msg = check_validity(board, player, move)

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