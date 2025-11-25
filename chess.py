# this is the main board which is being displayed to the user
board = [
    [-1, -2, -3, -4, -5, -3, -2, -1],
    [-6, -6, -6, -6, -6, -6, -6, -6],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [6, 6, 6, 6, 6, 6, 6, 6],
    [1, 2, 3, 4, 5, 3, 2, 1]
]

# deepcopy of board
tempboard = [row[:] for row in board]

# if player = 1, white moves else black (1 = White, 0 = Black)
player = 1

# to check if the game ended with a checkmate, stalemate or was resigned by someone
checkmate = 0
stalemate = 0
resigned = 0

# castling/movement flags
black_rook1_moved = 0
black_rook2_moved = 0
white_rook1_moved = 0
white_rook2_moved = 0
white_king_moved = 0
black_king_moved = 0

# ---------------- PRINT PROMPTS -------------------

def printInvalidMove():
    print("\033[31mInvalid move!\033[0m")

def printCheck():
    if player:
        print("\033[31mWhite is in CHECK!\033[0m")
    else:
        print("\033[31mBlack is in CHECK!\033[0m")

def printVictory():
    if player:
        print("\033[32mWhite wins!\033[0m")
    else:
        print("\033[32mBlack wins!\033[0m")

def printCheckmate():
    print("\033[32mCHECKMATE!\033[0m")

def printStalemate():
    print("\033[36mSTALEMATE!\033[0m")

def printThanks():
    print("\033[32mThanks for playing!\033[0m")

def printDraw():
    print("\033[36mGAME DRAWN\033[0m")

# --------------- PRINT BOARD (compact) ------------------

PIECES = {
    0: "   ",
    -1: " ♜ ",
    -2: " ♞ ",
    -3: " ♝ ",
    -4: " ♛ ",
    -5: " ♚ ",
    -6: " ♟ ",
     1: " ♖ ",
     2: " ♘ ",
     3: " ♗ ",
     4: " ♕ ",
     5: " ♔ ",
     6: " ♙ ",
}

def printBoard():
    col_name = ['a','b','c','d','e','f','g','h']
    # REAL dark brown RGB
    DARK_BROWN = "\x1b[48;2;139;69;19m"
    # REAL light brown RGB
    LIGHT_BROWN = "\x1b[48;2;205;133;63m"
    # White squares
    WHITE = "\x1b[47m"
    # Reset
    RESET = "\x1b[0m"

    # Top border (dark brown)
    print(DARK_BROWN + "   ", end="")
    for c in col_name:
        print(f" {c} ", end="")
    print("   " + RESET)
    for row in range(8):
        rank = 8 - row
        # Left border
        print(DARK_BROWN + f" {rank} " + RESET, end="")
        for col in range(8):
            # white + brown squares
            if (row + col) % 2 == 0:
                bg = WHITE
            else:
                bg = LIGHT_BROWN
            print(bg + PIECES[board[row][col]] + RESET, end="")
        # Right border
        print(DARK_BROWN + f" {rank} " + RESET)
    # Bottom border
    print(DARK_BROWN + "   ", end="")
    for c in col_name:
        print(f" {c} ", end="")
    print("   " + RESET)


# ---------------- MOVEMENT RULES (Chunk 2) ----------------

def whiteSoldierMove(Board, r1, c1, r2, c2):
    """whiteSoldierMove"""
    # forward moves
    if c1 == c2:
        # two-square from initial rank (r1 == 6 corresponds to chess rank 2)
        if (r1 == 6) and (Board[r2][c2] == 0) and (Board[r1 - 1][c2] == 0) and (r2 in (4, 5)):
            return True
        # single-square forward
        elif (r2 + 1) == r1 and (Board[r2][c2] == 0):
            return True
        else:
            return False
    # captures
    elif (Board[r2][c2] < 0) and (r2 == (r1 - 1)) and (c2 in (c1 - 1, c1 + 1)):
        return True
    else:
        return False


def blackSoldierMove(Board, r1, c1, r2, c2):
    """blackSoldierMove"""
    if c1 == c2:
        if (r1 == 1) and (Board[r2][c2] == 0) and (Board[r1 + 1][c2] == 0) and (r2 in (2, 3)):
            return True
        elif (r2 - 1) == r1 and (Board[r2][c2] == 0):
            return True
        else:
            return False
    elif (Board[r2][c2] > 0) and (r2 == (r1 + 1)) and (c2 in (c1 - 1, c1 + 1)):
        return True
    else:
        return False


def horseMove(Board, r1, c1, r2, c2):
    """Knight moves"""
    if player and Board[r2][c2] > 0:
        return False
    if (not player) and Board[r2][c2] < 0:
        return False
    if ((r2 in (r1 + 2, r1 - 2)) and (c2 in (c1 + 1, c1 - 1))) or \
       ((c2 in (c1 + 2, c1 - 2)) and (r2 in (r1 + 1, r1 - 1))):
        return True
    return False


def elephantMove(Board, r1, c1, r2, c2):
    """Rook moves"""
    # cannot capture same color
    if player and Board[r2][c2] > 0:
        return False
    if (not player) and Board[r2][c2] < 0:
        return False
    if r1 == r2:
        if c1 > c2:
            for i in range(c1 - 1, c2, -1):
                if Board[r2][i] != 0:
                    return False
            return True
        elif c2 > c1:
            for i in range(c1 + 1, c2):
                if Board[r2][i] != 0:
                    return False
            return True
        else:
            return False
    elif c1 == c2:
        if r1 > r2:
            for i in range(r1 - 1, r2, -1):
                if Board[i][c2] != 0:
                    return False
            return True
        elif r2 > r1:
            for i in range(r1 + 1, r2):
                if Board[i][c2] != 0:
                    return False
            return True
        else:
            return False
    else:
        return False


def camelMove(Board, r1, c1, r2, c2):
    """Bishop moves"""
    if player and Board[r2][c2] > 0:
        return False
    if (not player) and Board[r2][c2] < 0:
        return False

    dr = r2 - r1
    dc = c2 - c1

    if abs(dr) != abs(dc) or dr == 0:
        return False

    step_r = 1 if dr > 0 else -1
    step_c = 1 if dc > 0 else -1

    i, j = r1 + step_r, c1 + step_c
    while (i != r2) and (j != c2):
        if Board[i][j] != 0:
            return False
        i += step_r
        j += step_c
    return True


def isCastle(Board, r1, c1, r2, c2):
    """Ensures:
      - king is not currently in check
      - rook/king haven't moved and squares between are empty (existing checks)
      - the squares the king passes through AND the destination are NOT attacked
    """
    # First, king must not be in check
    if not isKingSafe(Board):
        return False

    # helper to test if a board where king is moved to (r,c) is safe
    def king_square_safe_after_move(orig_board, from_r, from_c, to_r, to_c):
        tb = [row[:] for row in orig_board]
        king_piece = tb[from_r][from_c]
        tb[from_r][from_c] = 0
        tb[to_r][to_c] = king_piece
        # use existing isKingSafe which expects current player global and looks for king of current player
        return isKingSafe(tb)

    # Black side castling (top of board)
    if r1 == 0 and c1 == 4:
        if black_king_moved:
            return False
        # kingside: target c2 == 6, rook at (0,7)
        if c2 == 6 and not black_rook2_moved and (Board[0][7] == -1):
            # squares between must be empty
            for i in range(c1 + 1, 7):
                if Board[r1][i] != 0:
                    return False
            # ensure squares king passes through are not attacked: c1 (already checked), c1+1 and c1+2
            # simulate king at c1+1 and c1+2
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 + 1):
                return False
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 + 2):
                return False
            return True
        # queenside: target c2 == 2, rook at (0,0)
        elif c2 == 2 and not black_rook1_moved and (Board[0][0] == -1):
            for i in range(c1 - 1, 0, -1):
                if Board[r1][i] != 0:
                    return False
            # ensure king squares c1-1 and c1-2 are safe
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 - 1):
                return False
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 - 2):
                return False
            return True

    # White side castling (bottom of board)
    if r1 == 7 and c1 == 4:
        if white_king_moved:
            return False
        # kingside: target c2 == 6, rook at (7,7)
        if c2 == 6 and not white_rook2_moved and (Board[7][7] == 1):
            for i in range(c1 + 1, 7):
                if Board[r1][i] != 0:
                    return False
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 + 1):
                return False
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 + 2):
                return False
            return True
        # queenside: target c2 == 2, rook at (7,0)
        elif c2 == 2 and not white_rook1_moved and (Board[7][0] == 1):
            for i in range(c1 - 1, 0, -1):
                if Board[r1][i] != 0:
                    return False
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 - 1):
                return False
            if not king_square_safe_after_move(Board, r1, c1, r1, c1 - 2):
                return False
            return True

    return False



def castle(r1, c1, r2, c2):
    """Perform castle (C castle) directly on global board"""
    global board
    if r1 == 0:
        if c2 == 6:
            board[0][7] = 0
            board[0][5] = -1
        elif c2 == 2:
            board[0][0] = 0
            board[0][3] = -1
    else:
        if c2 == 6:
            board[7][7] = 0
            board[7][5] = 1
        elif c2 == 2:
            board[7][0] = 0
            board[7][3] = 1


def kingMove(Board, r1, c1, r2, c2):
    """King move (handles castling by calling isCastle/castle)"""
    # allow castle if appropriate
    if r2 == r1 and not (c2 == c1 + 1 or c2 == c1 - 1):
        if isCastle(Board, r1, c1, r2, c2):
            castle(r1, c1, r2, c2)
            return True

    if player and Board[r2][c2] > 0:
        return False
    if (not player) and Board[r2][c2] < 0:
        return False

    if abs(r2 - r1) == 1 and abs(c2 - c1) == 1:
        return True
    if r2 == r1 and abs(c2 - c1) == 1:
        return True
    if c2 == c1 and abs(r2 - r1) == 1:
        return True
    return False


def pawn_promotion(r1, c1):
    """Promote pawn on board; determines color by the piece present at r1,c1"""
    global board
    piece = board[r1][c1]
    # piece > 0 => White pawn promoted
    if piece > 0:
        choices = {'Q': 4, 'H': 2, 'R': 1, 'B': 3}
        txt = "Enter Q for Queen, H for Horse, R for Rook, B for Bishop: "
        ch = input(txt).strip()
        if ch in choices:
            board[r1][c1] = choices[ch]
        else:
            print("Invalid input! Try again.")
            pawn_promotion(r1, c1)
    else:
        choices = {'q': -4, 'h': -2, 'r': -1, 'b': -3}
        txt = "Enter q for Queen, h for Horse, r for Rook, b for Bishop: "
        ch = input(txt).strip()
        if ch in choices:
            board[r1][c1] = choices[ch]
        else:
            print("Invalid input! Try again.")
            pawn_promotion(r1, c1)


# ---------------- MOVE VALIDATION & MAKE MOVE (Chunk 3) ----------------


def isValidMove(Board, r1, c1, r2, c2):
    """
    Checks that the piece at r1,c1 belongs to current player and that
    the requested move is valid according to piece-specific rules.
    """
    pawn = Board[r1][c1]

    # ensure there is a piece belonging to the current player
    if (player and pawn > 0) or ((not player) and pawn < 0):
        # white pawn (6) / black pawn (-6)
        if pawn == 6:
            return bool(whiteSoldierMove(Board, r1, c1, r2, c2))
        if pawn == -6:
            return bool(blackSoldierMove(Board, r1, c1, r2, c2))
        # king (5 / -5)
        if pawn == 5 or pawn == -5:
            return bool(kingMove(Board, r1, c1, r2, c2))
        # bishop-like (3 / -3)
        if pawn == 3 or pawn == -3:
            return bool(camelMove(Board, r1, c1, r2, c2))
        # knight (2 / -2)
        if pawn == 2 or pawn == -2:
            return bool(horseMove(Board, r1, c1, r2, c2))
        # rook (1 / -1)
        if pawn == 1 or pawn == -1:
            return bool(elephantMove(Board, r1, c1, r2, c2))
        # queen (4 / -4) -> rook OR bishop
        if pawn == 4 or pawn == -4:
            if elephantMove(Board, r1, c1, r2, c2) or camelMove(Board, r1, c1, r2, c2):
                return True
            return False
    return False


def makeMove(Board, r1, c1, r2, c2):
    """
    Perform move on Board (in-place). If the move leaves current player's king in check,
    revert and return False. Otherwise toggle player and return True.
    """
    global player

    temp = Board[r2][c2]
    Board[r2][c2] = Board[r1][c1]
    Board[r1][c1] = 0

    # if king not safe after this move -> revert
    if not isKingSafe(Board):
        Board[r1][c1] = Board[r2][c2]
        Board[r2][c2] = temp
        return False
    else:
        # toggle player
        player = 0 if player else 1
        return True


# ---------------- KING SAFETY & VALID MOVE SEARCH (Chunk 4) ----------------

def isKingSafe(Board):
    global player
    r = -1
    c = -1

    # locate the king of the *current* player
    for i in range(8):
        for j in range(8):
            if (Board[i][j] == 5 and player == 1) or (Board[i][j] == -5 and player == 0):
                r = i
                c = j
                break
        if r != -1:
            break

    if r == -1:
        # king not found (should never happen)
        return False

    # temporarily switch player to simulate opponent attacks
    if player == 1:
        player = 0
        for i in range(8):
            for j in range(8):
                if Board[i][j] >= 0:
                    continue
                if isValidMove(Board, i, j, r, c):
                    player = 1
                    return False
        player = 1
    else:
        player = 1
        for i in range(8):
            for j in range(8):
                if Board[i][j] <= 0:
                    continue
                if isValidMove(Board, i, j, r, c):
                    player = 0
                    return False
        player = 0

    return True


def playerHasValidMove():
    """
    Checks:
      • If any legal move exists for current player.
      • Updates tempboard.
      • Sets checkmate/stalemate flags.
    """
    global tempboard, board
    global checkmate, stalemate
    global player

    # sync tempboard
    for i in range(8):
        for j in range(8):
            tempboard[i][j] = board[i][j]

    # search moves
    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            # skip empty or opponent's pieces
            if piece == 0:
                continue
            if (player and piece < 0) or ((not player) and piece > 0):
                continue

            # try every target square
            for i in range(8):
                for j in range(8):
                    if isValidMove(board, r, c, i, j):
                        # simulate move on tempboard
                        saved1 = tempboard[i][j]
                        saved2 = tempboard[r][c]

                        tempboard[i][j] = tempboard[r][c]
                        tempboard[r][c] = 0

                        if isKingSafe(tempboard):
                            # restore and return valid
                            tempboard[i][j] = saved1
                            tempboard[r][c] = saved2
                            return True

                        # revert
                        tempboard[i][j] = saved1
                        tempboard[r][c] = saved2

    # if no moves, determine if it's checkmate or stalemate
    if not isKingSafe(board):
        checkmate = 1
    else:
        stalemate = 1

    # toggle player like C code
    player = 0 if player else 1

    return False


# ---------------- MAIN GAME LOOP (Chunk 5) ----------------

def main():
    global player, checkmate, stalemate, resigned
    global black_rook1_moved, black_rook2_moved, white_rook1_moved, white_rook2_moved
    global white_king_moved, black_king_moved

    # initialize flags
    black_rook1_moved = black_rook2_moved = 0
    white_rook1_moved = white_rook2_moved = 0
    white_king_moved = black_king_moved = 0
    player = 1
    checkmate = stalemate = resigned = 0

    
    # We use try/except here to prevent the entire game from crashing. Exceptions ensures the program continues or exits gracefully instead of stopping abruptly.
    # initialize Moves file
    try:
        with open("Moves.txt", "w") as f:
            f.write("\n-----------------PREVIOUS GAME'S MOVES---------------------\n")
    except Exception as e:
        print("Warning: could not initialize Moves.txt:", e)

    # optional instructions file display
    try:
        ans = input("Do you want to read the instructions? (y/n) - ").strip()
        if ans and ans[0].lower() == 'y':
            try:
                with open("instructions.txt", "r") as f:
                    print(f.read())
            except FileNotFoundError:
                print("instructions.txt not found.")
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return

    input("Press enter key to continue.... ")

    # main loop
    while playerHasValidMove():
        printBoard()
        if not isKingSafe(board):
            printCheck()

        print(f"{'White' if player else 'Black'}'s turn")
        move = input("Enter your move - ").strip()
        # handle resignation
        if len(move) == 1 and move.lower() == 'r':
            resigned = 1
            break

        # understanding moves like "e2e4"
        if len(move) == 4 and move[0].isalpha() and move[2].isalpha() and move[1].isdigit() and move[3].isdigit():
            # convert file letters to columns 0..7
            col_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
            a0 = move[0].lower()
            a2 = move[2].lower()
            if a0 not in col_map or a2 not in col_map:
                printInvalidMove()
                continue
            start_col = col_map[a0]
            end_col = col_map[a2]
            # convert ranks to rows: rank '8' -> row 0
            # row index = 8 - rank
            try:
                start_row = 8 - int(move[1])
                end_row = 8 - int(move[3])
            except ValueError:
                printInvalidMove()
                continue
            # validate rows are 0..7
            if not (0 <= start_row < 8 and 0 <= end_row < 8):
                printInvalidMove()
                continue

            if isValidMove(board, start_row, start_col, end_row, end_col):
                # perform the move first (it will be rejected if it leaves king in check)
                if makeMove(board, start_row, start_col, end_row, end_col):
                    # After a successful move, check for pawn promotion on the destination square
                    moved_piece = board[end_row][end_col]
                    if moved_piece == 6 and end_row == 0:
                        pawn_promotion(end_row, end_col)
                    elif moved_piece == -6 and end_row == 7:
                        pawn_promotion(end_row, end_col)

                    # storing moves
                    try:
                        with open("Moves.txt", "a") as f:
                            f.write(f"{'White' if not player else 'Black'}'s move - {move[:4]}\n")
                    except Exception as e:
                        print("Warning: could not write moves:", e)

                    # update moved-piece flags
                    moved_piece = board[end_row][end_col]
                    if moved_piece == 5 or moved_piece == -5:
                        # note: player was toggled in makeMove
                        if not player:
                            white_king_moved = 1
                        else:
                            black_king_moved = 1
                    if moved_piece == 1 or moved_piece == -1:
                        # determine which rook moved by checking start position
                        if start_row == 0 and start_col == 0:
                            black_rook1_moved = 1
                        elif start_row == 0 and start_col == 7:
                            black_rook2_moved = 1
                        elif start_row == 7 and start_col == 0:
                            white_rook1_moved = 1
                        elif start_row == 7 and start_col == 7:
                            white_rook2_moved = 1
                    continue
                else:
                    printInvalidMove()
                    print(f"\n {'White' if player else 'Black'} king gets into check !\n")
            else:
                printInvalidMove()
        else:
            printInvalidMove()


    # end of play - print board and results
    printBoard()
    try:
        with open("Moves.txt", "a") as f:
            if checkmate:
                printCheckmate()
                printVictory()
                f.write(f"{'White' if player else 'Black'} won by checkmate\n")
            elif stalemate:
                printStalemate()
                printDraw()
                f.write("Match drawn by stalemate\n")
            elif resigned:
                f.write(f"{'White' if player else 'Black'} resigned\n")
                f.write(f"{'White' if not player else 'Black'} won\n")
                # switch player 
                player = 0 if player else 1
                printVictory()
    except Exception as e:
        print("Warning: could not write final result to Moves.txt:", e)

    printThanks()

main()
