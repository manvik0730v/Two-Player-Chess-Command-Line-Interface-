# **Team: Magnoos Carlsoon**

# **PyChess (Two Player Chess Game)**

A simple two-player chess game playable entirely from the terminal.  
White begins the game, and players alternate turns until the match ends.

---

### Rules

* The player using white pieces is called **White**.  
* The player using black pieces is called **Black**.  
* **White moves first.**
* Players **must** make a move each turn (skipping a turn is not allowed).
* The game ends when:
  - A **checkmate** occurs,  
  - A **stalemate** is reached,  
  - Or a player **resigns** by entering `r` or `R`.

* Supports:
  - Castling  
  - Pawn promotion  
  - Check and checkmate detection  
  - Standard movement rules  
* Does *not* support:
  - En passant  
  - Move timers  
  - AI / single-player mode  

### Concepts Used in This Chess Program
* Data Structures
 2D Lists (Matrix Representation):
The chessboard is stored as an 8×8 list of lists where each element represents a piece using a numeric code.
Integer Encoding for Pieces:
Positive numbers for White, negative numbers for Black; magnitude identifies piece type (King, Queen, Rook, Knight, Bishop, Pawn).

* Board Rendering
Displays the board in a user-friendly ASCII/terminal format.
Converts numerical pieces into readable symbols or characters.

* Error Handling
Invalid moves show error messages.
Program re-prompts without crashing.

* Modular functions for readability

* No external libraries used. No external dependencies required.


### How to run
* Run the below command in terminal
python3 chess.py

### Authors
1. Debmalya Rath
2. Manvik Kumar Gupta
3. Mohmad Abdul 
