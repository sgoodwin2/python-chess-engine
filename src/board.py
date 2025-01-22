class Board:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.white_king_moved = False
        self.white_rook_a_moved = False  # Rook on the a-file (left side)
        self.white_rook_h_moved = False  # Rook on the h-file (right side)
        self.black_king_moved = False
        self.black_rook_a_moved = False
        self.black_rook_h_moved = False
        self.previous_move = ((None, None), None)
        self.en_passant_target = None  # Initially no en passant target

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += " ".join(row) + "\n"
        return board_str

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        else:
            return '.'  # Return empty square indicator for out-of-bounds positions

    def set_piece(self, row, col, piece):
        if 0 <= row < 8 and 0 <= col < 8:
            if piece == 'K':
                self.white_king_moved = True
            elif piece == 'k':
                self.black_king_moved = True
            elif row == 7 and col == 0 and piece == 'R':
                self.white_rook_a_moved = True
            elif row == 7 and col == 7 and piece == 'R':
                self.white_rook_h_moved = True
            elif row == 0 and col == 0 and piece == 'r':
                self.black_rook_a_moved = True
            elif row == 0 and col == 7 and piece == 'r':
                self.black_rook_h_moved = True
            self.board[row][col] = piece
        else:
            raise IndexError("Board index out of range")
        if self.previous_move[0][0] is not None:
            if piece.upper() == 'P' and abs(row - self.previous_move[0][0]) == 2:
                self.en_passant_target = (row - 1 if piece.isupper() else row + 1, col)
            else:
                self.en_passant_target = None
        self.previous_move = ((row,col), piece)
        
        
    def get_pieces_of_color(self, color):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece != '.' and (color == 'white' and piece.isupper() or color == 'black' and piece.islower()):
                    pieces.append(((row, col), piece))
        return pieces
    
    def is_square_attacked(self, row, col, attacking_color):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece != '.':
                    piece_color = 'white' if piece.isupper() else 'black'
                    if piece_color == attacking_color:
                        if piece.upper() == 'P':
                            if attacking_color == 'white':
                                if (r + 1 == row and (c - 1 == col or c + 1 == col)):
                                    return True
                            else:
                                if (r - 1 == row and (c - 1 == col or c + 1 == col)):
                                    return True
                        elif piece.upper() == 'R':
                            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                for i in range(1, 8):
                                    nr, nc = r + dr * i, c + dc * i
                                    if nr == row and nc == col:
                                        return True
                                    if self.get_piece(nr, nc) != '.' :
                                        break
                        elif piece.upper() == 'N':
                            for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                                nr, nc = r + dr, c + dc
                                if nr == row and nc == col:
                                    return True
                        elif piece.upper() == 'B':
                            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                                for i in range(1, 8):
                                    nr, nc = r + dr * i, c + dc * i
                                    if nr == row and nc == col:
                                        return True
                                    if self.get_piece(nr, nc) != '.':
                                        break
                        elif piece.upper() == 'Q':
                            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                                for i in range(1, 8):
                                    nr, nc = r + dr * i, c + dc * i
                                    if nr == row and nc == col:
                                        return True
                                    if self.get_piece(nr, nc) != '.':
                                        break
                        elif piece.upper() == 'K':
                            for dr, dc in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                                nr, nc = r + dr, c + dc
                                if nr == row and nc == col:
                                    return True
        return False