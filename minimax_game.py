import sys
import copy

class TicTacToeMatrix:
    """Manages the grid matrix state and evaluates tactical win states."""
    def __init__(self):
        # Represent a 3x3 grid as a flat list of 9 elements
        self.board = [" " for _ in range(9)]
        self.ai_marker = "O"
        self.human_marker = "X"

    def print_board(self):
        """Renders the board matrix cleanly to the stdout terminal."""
        print("\n")
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            print(" | ".join(row))
            if i < 2:
                print("---------")
        print("\n")

    def get_available_moves(self, state_board) -> list:
        return [index for index, cell in enumerate(state_board) if cell == " "]

    def check_win_condition(self, state_board, marker) -> bool:
        """Evaluates all 8 standard geometric vectors for a win condition."""
        win_vectors = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for vector in win_vectors:
            if all(state_board[cell] == marker for cell in vector):
                return True
        return False

    def is_board_full(self, state_board) -> bool:
        return " " not in state_board

    # =====================================================================
    # THE MINIMAX ALGORITHMIC RECURSION ENGINE
    # =====================================================================
    def minimax(self, state_board, depth, is_maximizing) -> int:
        """Recursively parses downstream choice vectors to find optimum path weights."""
        
        # Base Cases: Score terminal leaf nodes
        if self.check_win_condition(state_board, self.ai_marker):
            return 10 - depth  # AI wins (prefer faster wins)
        if self.check_win_condition(state_board, self.human_marker):
            return depth - 10  # Human wins (prefer delaying losses)
        if self.is_board_full(state_board):
            return 0           # Draw

        if is_maximizing:
            best_score = -float('inf')
            # Loop through all possible future branches
            for move in self.get_available_moves(state_board):
                state_board[move] = self.ai_marker # Simulate move
                score = self.minimax(state_board, depth + 1, False) # Recurse down
                state_board[move] = " " # Backtrack / Reset board state
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_available_moves(state_board):
                state_board[move] = self.human_marker # Simulate opponent counter-move
                score = self.minimax(state_board, depth + 1, True) # Recurse down
                state_board[move] = " " # Backtrack
                best_score = min(score, best_score)
            return best_score

    def calculate_optimum_move(self) -> int:
        """Triggers the root calculation loop to identify the single best move index."""
        best_score = -float('inf')
        target_move = None
        
        for move in self.get_available_moves(self.board):
            self.board[move] = self.ai_marker
            move_score = self.minimax(self.board, 0, False)
            self.board[move] = " "
            
            if move_score > best_score:
                best_score = move_score
                target_move = move
                
        return target_move

# =====================================================================
# SYSTEM EXECUTION INTERFACE
# =====================================================================
def start_game_match():
    game = TicTacToeMatrix()
    print("🤖 Unbeatable AI Matrix Engine Activated. Human Player: [X] | AI: [O]")
    game.print_board()

    while not game.is_board_full(game.board):
        # --- HUMAN TURN PHASE ---
        available = game.get_available_moves(game.board)
        user_input = None
        while user_input not in available:
            try:
                user_input = int(input(f"Enter target grid index choice {available}: "))
            except ValueError:
                continue
        
        game.board[user_input] = game.human_marker
        game.print_board()
        
        if game.check_win_condition(game.board, game.human_marker):
            print("🎉 Impossible achievement! Human wins.")
            sys.exit()
            
        if game.is_board_full(game.board):
            break

        # --- AI TURN PHASE ---
        print("🧠 AI is computing optimal matrix futures...")
        ai_choice = game.calculate_optimum_move()
        if ai_choice is not None:
            game.board[ai_choice] = game.ai_marker
            game.print_board()
            
        if game.check_win_condition(game.board, game.ai_marker):
            print("💀 Match Terminated. AI Wins. The game logic is mathematically flawless.")
            sys.exit()

    print("🏁 Deadlock condition met. The match is a structural Draw.")

if __name__ == "__main__":
    start_game_match()
