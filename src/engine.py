from board import Board
import time

def generate_pawn_moves(board, row, col, color):
    moves = []
    if color == 'white':
        # One square forward
        if board.get_piece(row - 1, col) == '.':
            moves.append(((row, col), (row - 1, col)))
            # Two squares forward (if on starting rank)
            if row == 6 and board.get_piece(row - 2, col) == '.':
                moves.append(((row, col), (row - 2, col)))
        # Captures
        piece = board.get_piece(row - 1, col - 1)
        if piece != '.' and piece.islower():
            moves.append(((row, col), (row - 1, col - 1)))
        piece = board.get_piece(row - 1, col + 1)
        if piece != '.' and piece.islower():
            moves.append(((row, col), (row - 1, col + 1)))
        if board.en_passant_target:
            ep_row, ep_col = board.en_passant_target
            if row == 3 and (col - 1 == ep_col or col + 1 == ep_col):
                moves.append(((row, col), (ep_row, ep_col)))
        if row == 0:  # Promotion for white
            for piece in ['Q', 'R', 'B', 'N']:
                moves.append(((row+1, col), (row, col), piece))
    elif color == 'black':
        # One square forward
        if board.get_piece(row + 1, col) == '.':
            moves.append(((row, col), (row + 1, col)))
            # Two squares forward (if on starting rank)
            if row == 1 and board.get_piece(row + 2, col) == '.':
                moves.append(((row, col), (row + 2, col)))
        # Captures
        piece = board.get_piece(row + 1, col - 1)
        if piece != '.' and piece.isupper():
            moves.append(((row, col), (row + 1, col - 1)))
        piece = board.get_piece(row + 1, col + 1)
        if piece != '.' and piece.isupper():
            moves.append(((row, col), (row + 1, col + 1)))
        if board.en_passant_target:
            ep_row, ep_col = board.en_passant_target
            if row == 4 and (col - 1 == ep_col or col + 1 == ep_col):
                moves.append(((row, col), (ep_row, ep_col)))
        if row == 7:  # Promotion for black
            for piece in ['q', 'r', 'b', 'n']:
                moves.append(((row-1, col), (row, col), piece))
    return moves

def generate_rook_moves(board, row, col, color):
    moves = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Directions: right, left, down, up
        for i in range(1, 8):  # Check up to 7 squares in each direction
            new_row, new_col = row + dr * i, col + dc * i
            piece = board.get_piece(new_row, new_col)
            if piece == '.':
                moves.append(((row, col), (new_row, new_col)))
            elif (color == 'white' and piece.islower()) or (color == 'black' and piece.isupper()): # capture
                moves.append(((row, col), (new_row, new_col)))
                break  # Stop after capturing an opponent's piece
            else:
                break  # Stop if blocked by own piece
    return moves

def generate_knight_moves(board, row, col, color):
    moves = []
    for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
        new_row, new_col = row + dr, col + dc
        piece = board.get_piece(new_row, new_col)
        if piece == '.' or (color == 'white' and piece.islower()) or (color == 'black' and piece.isupper()):
            moves.append(((row, col), (new_row, new_col)))
    return moves

def generate_bishop_moves(board, row, col, color):
    moves = []
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Diagonal directions
        for i in range(1, 8):
            new_row, new_col = row + dr * i, col + dc * i
            piece = board.get_piece(new_row, new_col)
            if piece == '.':
                moves.append(((row, col), (new_row, new_col)))
            elif (color == 'white' and piece.islower()) or (color == 'black' and piece.isupper()):
                moves.append(((row, col), (new_row, new_col)))
                break
            else:
                break
    return moves

def generate_queen_moves(board, row, col, color):
    # Queen moves are the combination of rook and bishop moves
    moves = generate_rook_moves(board, row, col, color) + generate_bishop_moves(board, row, col, color)
    return moves

def generate_king_moves(board, row, col, color):
    moves = []
    # Regular king moves
    for dr, dc in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
        new_row, new_col = row + dr, col + dc
        piece = board.get_piece(new_row, new_col)
        if piece == '.' or (color == 'white' and piece.islower()) or (color == 'black' and piece.isupper()):
            moves.append(((row, col), (new_row, new_col)))

    # Castling (Now outside the regular move generation loop)
    if color == 'white' and not board.white_king_moved:
        if (not board.white_rook_h_moved and
            board.get_piece(7, 5) == '.' and
            board.get_piece(7, 6) == '.' and
            not board.is_square_attacked(7, 4, 'black') and
            not board.is_square_attacked(7, 5, 'black')): #and not board.is_square_attacked(7, 6, 'black'): Removed this check as it is redundant
            moves.append(((7, 4), (7, 6)))  # Kingside castling
        if (not board.white_rook_a_moved and
            board.get_piece(7, 1) == '.' and
            board.get_piece(7, 2) == '.' and
            board.get_piece(7,3) == '.' and
            not board.is_square_attacked(7, 4, 'black') and
            not board.is_square_attacked(7, 3, 'black')): #and not board.is_square_attacked(7, 2, 'black'): Removed this check as it is redundant
            moves.append(((7, 4), (7, 2)))  # Queenside castling
    elif color == 'black' and not board.black_king_moved:
        if (not board.black_rook_h_moved and
            board.get_piece(0, 5) == '.' and
            board.get_piece(0, 6) == '.' and
            not board.is_square_attacked(0, 4, 'white') and
            not board.is_square_attacked(0, 5, 'white')): #and not board.is_square_attacked(0, 6, 'white'): Removed this check as it is redundant
            moves.append(((0, 4), (0, 6)))  # Kingside castling
        if (not board.black_rook_a_moved and
            board.get_piece(0, 1) == '.' and
            board.get_piece(0, 2) == '.' and
            board.get_piece(0,3) == '.' and
            not board.is_square_attacked(0, 4, 'white') and
            not board.is_square_attacked(0, 3, 'white')): #and not board.is_square_attacked(0, 2, 'white'): Removed this check as it is redundant
            moves.append(((0, 4), (0, 2)))  # Queenside castling

    return moves

def is_legal_move(board, move, current_color):
    start_row, start_col = move[0]
    end_row, end_col = move[1]
    promotion_piece = None
    if len(move) == 3:
        promotion_piece = move[2]
    # Initialize captured_piece *before* the if statement.
    captured_piece = '.'  # Default to empty square
    piece = board.get_piece(start_row, start_col)

    if 0 <= end_row < 8 and 0 <= end_col < 8:  # Check if destination is within board bounds
        board.set_piece(start_row, start_col, '.')
        captured_piece = board.get_piece(end_row, end_col)
        board.set_piece(end_row, end_col, piece)
        if piece.upper() == 'K' and abs(start_col - end_col) == 2:  # Castling move
            rook_col = 7 if end_col == 6 else 0
            rook_end_col = 5 if end_col == 6 else 3
            rook = 'R' if current_color == 'white' else 'r'
            board.set_piece(start_row, rook_col, '.')
            board.set_piece(start_row, rook_end_col, rook)
        if piece.upper() == 'P' and end_col != start_col and captured_piece == '.': #En Passant
            board.set_piece(start_row, end_col, '.')
        if promotion_piece is not None:
            board.set_piece(end_row, end_col, promotion_piece)
    else:
        return False  # Move is off the board, so it is illegal

    # Find the king's position
    king_row, king_col = -1, -1
    for r in range(8):
        for c in range(8):
            p = board.get_piece(r, c)
            if p == ('K' if current_color == 'white' else 'k'):
                king_row, king_col = r, c
                break
        if king_row != -1:
            break

    # Check if the king is now in check
    opponent_color = 'black' if current_color == 'white' else 'white'
    is_in_check = board.is_square_attacked(king_row, king_col, opponent_color)

    # Undo the move
    board.set_piece(start_row, start_col, piece)
    board.set_piece(end_row, end_col, captured_piece)
    if piece.upper() == 'K' and abs(start_col - end_col) == 2: #Undo castling move
        rook_col = 7 if end_col == 6 else 0
        rook_end_col = 5 if end_col == 6 else 3
        board.set_piece(start_row, rook_end_col, '.')
        board.set_piece(start_row, rook_col, 'R' if current_color == 'white' else 'r')
    if piece.upper() == 'P' and end_col != start_col and captured_piece == '.': #Undo En Passant
        board.set_piece(start_row, end_col, 'p' if current_color == 'white' else 'P')
    if promotion_piece is not None:
        board.set_piece(end_row, end_col, 'P' if current_color == 'white' else 'p')
    return not is_in_check

def evaluate(board):
    score = 0
    piece_values = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 100,
                    'p': -1, 'r': -5, 'n': -3, 'b': -3, 'q': -9, 'k': -100}  # Piece values
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece != '.':
                score += piece_values[piece]
    return score

def undo_move(board, move, current_color, captured_piece):
    start_row, start_col = move[0]
    end_row, end_col = move[1]
    promotion_piece = None
    if len(move) == 3:
        promotion_piece = move[2]
    piece = board.get_piece(end_row, end_col)
    board.set_piece(end_row, end_col, captured_piece)
    board.set_piece(start_row, start_col, piece)
    if piece.upper() == 'K' and abs(start_col - end_col) == 2: #Undo castling move
        rook_col = 7 if end_col == 6 else 0
        rook_end_col = 5 if end_col == 6 else 3
        board.set_piece(start_row, rook_end_col, '.')
        board.set_piece(start_row, rook_col, 'R' if current_color == 'white' else 'r')
    if piece.upper() == 'P' and end_col != start_col and captured_piece == '.': #Undo En Passant
        board.set_piece(start_row, end_col, 'p' if current_color == 'white' else 'P')
    if promotion_piece is not None:
        board.set_piece(end_row, end_col, 'P' if current_color == 'white' else 'p')

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in get_all_possible_moves(board, 'white'):
            if is_legal_move(board, move, 'white'):
                captured_piece = make_move(board, move, 'white')
                eval = minimax(board, depth - 1, alpha, beta, False)
                undo_move(board, move, 'white', captured_piece)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)  # Alpha update
                if beta <= alpha:  # Beta cutoff
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_possible_moves(board, 'black'):
            if is_legal_move(board, move, 'black'):
                captured_piece = make_move(board, move, 'black')
                eval = minimax(board, depth - 1, alpha, beta, True)
                undo_move(board, move, 'black', captured_piece)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)  # Beta update
                if beta <= alpha:  # Alpha cutoff
                    break
        return min_eval

def get_all_possible_moves(board, color):
    moves = []
    pieces = board.get_pieces_of_color(color)
    for position, piece in pieces:
        if piece.upper() == "P":
            moves.extend(generate_pawn_moves(board, position[0], position[1], color))
        elif piece.upper() == "R":
            moves.extend(generate_rook_moves(board, position[0], position[1], color))
        elif piece.upper() == "N":
            moves.extend(generate_knight_moves(board, position[0], position[1], color))
        elif piece.upper() == "B":
            moves.extend(generate_bishop_moves(board, position[0], position[1], color))
        elif piece.upper() == "Q":
            moves.extend(generate_queen_moves(board, position[0], position[1], color))
        elif piece.upper() == "K":
            moves.extend(generate_king_moves(board, position[0], position[1], color))
    return moves

def make_move(board, move, current_color):
    start_row, start_col = move[0]
    end_row, end_col = move[1]
    promotion_piece = None
    if len(move) == 3:
        promotion_piece = move[2]
    piece = board.get_piece(start_row, start_col)
    board.set_piece(start_row, start_col, '.')
    captured_piece = board.get_piece(end_row, end_col)
    board.set_piece(end_row, end_col, piece)
    if piece.upper() == 'K' and abs(start_col - end_col) == 2:  # Castling move
        rook_col = 7 if end_col == 6 else 0
        rook_end_col = 5 if end_col == 6 else 3
        rook = 'R' if current_color == 'white' else 'r'
        board.set_piece(start_row, rook_col, '.')
        board.set_piece(start_row, rook_end_col, rook)
    if piece.upper() == 'P' and end_col != start_col and captured_piece == '.': #En Passant
        board.set_piece(start_row, end_col, '.')
    if promotion_piece is not None:
        board.set_piece(end_row, end_col, promotion_piece)
    return captured_piece

def find_best_move(board, depth):
    alpha = -float('inf')
    beta = float('inf')
    best_eval = -float('inf')
    best_move = None
    for move in get_all_possible_moves(board, 'white'):
        if is_legal_move(board, move, 'white'):
            captured_piece = make_move(board, move, 'white')
            eval = minimax(board, depth - 1, alpha, beta, False)
            undo_move(board, move, 'white', captured_piece)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            alpha = max(alpha, eval)
    return best_move

def play_game():
    board = Board()
    current_player = 'white'
    game_over = False
    move_number = 1

    while not game_over:
        print(f"\nMove {move_number}: {current_player.upper()}'s turn")
        print(board)

        if current_player == 'white':
            move = find_best_move(board, 3)  # AI Move
            if move is None:
                if is_check(board, 'white'):
                    print("Checkmate, Black Wins")
                else:
                    print("Stalemate")
                game_over = True
                continue
            print(f"White plays {move}")
            captured_piece = make_move(board, move, current_player)
            
        else:
            while True:
                try:
                    move_str = input("Enter your move (e.g., e2e4 or e7e8Q for promotion): ")
                    if len(move_str) == 4:
                        start_col = ord(move_str[0]) - ord('a')
                        start_row = 8 - int(move_str[1])
                        end_col = ord(move_str[2]) - ord('a')
                        end_row = 8 - int(move_str[3])
                        moves = get_all_possible_moves(board, current_player)
                        move = None
                        for possible_move in moves:
                            if possible_move[0] == (start_row, start_col) and possible_move[1] == (end_row, end_col):
                                if is_legal_move(board, possible_move, current_player):
                                    move = possible_move
                                    break
                        if move is not None:
                            captured_piece = make_move(board, move, current_player)
                            break
                        else:
                            print("Invalid Move")
                    elif len(move_str) == 5:
                        start_col = ord(move_str[0]) - ord('a')
                        start_row = 8 - int(move_str[1])
                        end_col = ord(move_str[2]) - ord('a')
                        end_row = 8 - int(move_str[3])
                        promotion_piece = move_str[4]
                        moves = get_all_possible_moves(board, current_player)
                        move = None
                        for possible_move in moves:
                            if possible_move[0] == (start_row, start_col) and possible_move[1] == (end_row, end_col) and len(possible_move) == 3 and possible_move[2].upper() == promotion_piece.upper():
                                if is_legal_move(board, possible_move, current_player):
                                    move = possible_move
                                    break
                        if move is not None:
                            captured_piece = make_move(board, move, current_player)
                            break
                        else:
                            print("Invalid Move")
                    else:
                        print("Invalid move format. Use algebraic notation (e.g., e2e4 or e7e8Q for promotion).")
                except ValueError:
                    print("Invalid move format. Use algebraic notation (e.g., e2e4 or e7e8Q for promotion).")
                except IndexError:
                    print("Invalid move format. Use algebraic notation (e.g., e2e4 or e7e8Q for promotion).")
        if is_check(board, 'black' if current_player == 'white' else 'white'):
            print("Check")
        current_player = 'black' if current_player == 'white' else 'white'
        move_number += 1

def is_check(board, color):
    king_row, king_col = -1, -1
    for r in range(8):
        for c in range(8):
            p = board.get_piece(r,c)
            if p == ('K' if color == 'white' else 'k'):
                king_row, king_col = r, c
                break
        if king_row != -1:
            break
    opponent_color = 'black' if color == 'white' else 'white'
    return board.is_square_attacked(king_row, king_col, opponent_color)

def main():
    play_game()

if __name__ == "__main__":
    main()