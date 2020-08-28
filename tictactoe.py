# a3.py

import random
import sys


class TicTacToe:
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Board state ('1' = X, '-1' = O, '1' == empty)
    turn = "player"  # '1' is player and '2' is computer
    end = False  # Has the game ended?
    player_display_code = 1  # "X"
    computer_display_code = -1  # "O"

    def __init__(self):
        self.reset()

    # Reset the state of the game
    def reset(self):

        print("----- NEW GAME INITIALIZED ------")

        # Empty the board slots
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Prompt the user to choose a turn
        self.turn = input("Enter '1' to play first, '2' or enter to play second:")
        if self.turn == '1':
            self.turn = "player"
        elif self.turn == '2':
            self.turn = "computer"
        else:
            self.turn = "computer"

        # Prompt the user to choose whether they're an 'X' or 'O' (coded as 1 and -1, respectively)
        self.player_display_code = input("Select what your play as ('X' or 'O'):")
        if self.player_display_code.lower() == "x":
            self.player_display_code = 1
            self.computer_display_code = -1
        else:
            self.player_display_code = -1
            self.computer_display_code = 1

        # Set the game to a non-ending state
        self.end = False

        # Print newlines
        print("\n\n")

    # Return 'X', 'O', or the current position number if it's empty
    def get_display_char(self, pos: int) -> str:
        status = self.board[pos]
        if status == 0:
            return str(pos)
        elif status == 1:
            return "\033[94m" + "X" + "\033[0m"
        else:
            return "\033[91m" + "O" + "\033[0m"

    def display(self):
        for i in range(len(self.board)):
            # Don't print a bar if we're on the last column
            if (i + 1) % 3 == 0:
                # Print current position
                print(self.get_display_char(i))
                # Print separator row if we're not on the last row
                if i != (len(self.board) - 1):
                    print("-----")
            else:
                # Print current position
                print(self.get_display_char(i), end="|")

    @staticmethod
    def check_win(board: list) -> (bool, int):
        def check_column(pos: int) -> bool:
            # get col number
            col = pos % 3
            # first col
            if col == 0:
                return board[0] == board[3] == board[6] and board[0] != 0
            # second col
            elif col == 1:
                return board[1] == board[4] == board[7] and board[1] != 0
            # third col
            elif col == 2:
                return board[2] == board[5] == board[8] and board[2] != 0
            else:
                raise ValueError("Invalid column for position:", pos)

        def check_row(pos: int) -> bool:
            # first row
            if pos < 3:
                return board[0] == board[1] == board[2] and board[0] != 0
            # second row
            elif pos < 6:
                return board[3] == board[4] == board[5] and board[3] != 0
            # third row
            elif pos < 9:
                return board[6] == board[7] == board[8] and board[6] != 0
            else:
                raise ValueError("Invalid row for position:", pos)

        def check_diagonals(pos: int) -> bool:
            possible_winning_pos = [0, 2, 4, 6, 8]
            # If pos is in the possibly winning diagonals
            if pos in possible_winning_pos:
                left_diag = [0, 4, 8]
                right_diag = [2, 4, 6]

                if pos in left_diag:
                    return board[0] == board[4] == board[8] and board[4] != 0
                elif pos in right_diag:
                    return board[2] == board[4] == board[6] and board[4] != 0
                else:
                    raise ValueError("Unsupported position.")
            else:
                return False

        # For each position within the board
        for i in range(len(board)):
            if board[i] != 0:
                # Check if there is a win including this current position
                if check_column(i) or check_row(i) or check_diagonals(i):
                    # return True and the position
                    return True, i

        # Return False and no position
        return False, None

    def restart(self):
        self.reset()

    @staticmethod
    def get_legal_moves(board: list) -> list:
        legal_moves = []

        # For each position on the board
        for i in range(9):
            # Add it to the list of legal moves if it's not occupied (if not equal to 1 or -1)
            if board[i] == 0:
                legal_moves.append(str(i))
        return legal_moves

    def get_best_move(self) -> int:

        # Dictionary holding a legal move (key) and the number of wins (value) its random playouts produced
        move_wins = {}

        # Get a list of legal moves
        legal_moves = self.get_legal_moves(self.board)

        # The number of random playouts we will do for each legal move
        playouts = 10000

        # Initialize the dictionary with 0's for each legal move
        for move in legal_moves:
            move_wins[move] = 0

        # Perform a random playout with Monte Carlo Tree Search
        def mct_playout(board, initial_move, turn):

            # Check if there's a winner, and the position a win was detected from
            win, winning_pos = TicTacToe.check_win(board)
            if win:
                # Check if the computer has won
                if board[winning_pos] == self.computer_display_code:
                    # Record that this playout is a win
                    move_wins[initial_move] += 2
                else:
                    # If the player has won
                    move_wins[initial_move] -= 5
                return

            # Get a list of legal moves for the current board state
            lm = TicTacToe.get_legal_moves(board)

            # Check if it's a draw
            if len(lm) == 0:
                move_wins[initial_move] += 1
                return

            # Choose a random legal move
            rnd_move = lm[random.randint(0, len(lm) - 1)]

            # Perform the legal move
            board[int(rnd_move)] = turn

            # Recurse
            return mct_playout(board, initial_move, turn * (-1))

        # Do x number of playouts for each legal move
        for move in legal_moves:
            for i in range(playouts):
                # Make a copy of the current board to avoid changing its state while we do the playouts
                board_copy = self.board.copy()

                # Perform the legal move
                board_copy[int(move)] = self.computer_display_code

                # Do a random playout
                mct_playout(board_copy, move, self.player_display_code)

        # Get a random move, which will be replaced with the move that produced most random playout wins
        winning_move = ""
        most_wins = -sys.maxsize - 1
        for move, wins in move_wins.items():
            if wins >= most_wins:
                winning_move = move
                most_wins = wins

        # Return the best move for the computer
        return winning_move

    def do_computer_turn(self):

        # Figure out what the next position should be
        next_pos = self.get_best_move()

        # Perform the move
        self.board[int(next_pos)] = self.computer_display_code

        # Pass the turn back to the player
        self.turn = "player"

    def do_player_turn(self):

        # Display the current state
        self.display()

        # Get the user's input
        next_pos = input("Please select your next position:")

        # Check if it's a valid input (a legal position to choose are their next move)
        while next_pos not in self.get_legal_moves(self.board):
            # Prompt user to re-enter a valid position
            next_pos = input("Invalid position chosen, please select your next position:")

        # Set the position
        self.board[int(next_pos)] = self.player_display_code

        # Pass the turn back to the computer
        self.turn = "computer"

    def play_turn(self):

        # Check if there's a winner, and the position a win was detected from
        win, winner_pos = self.check_win(self.board)

        # If someone has already won or it's a draw
        if win or len(self.get_legal_moves(self.board)) == 0:

            # Set self.end to true to stop the loop
            self.end = True

            # Display the current state
            self.display()

            # If there is a winner
            if winner_pos is not None:
                # Determine the winner
                if self.board[winner_pos] == self.player_display_code:
                    print("Player has won.")
                elif self.board[winner_pos] == self.computer_display_code:
                    print("Computer has won.")
            else:
                print("Draw.")

            # Add newlines
            print("\n\n\n")

            # Check if the player would like to start a new game
            restart = input("Press 'P' to play again, anything else to quit")
            if restart.lower() == "p":

                # Restart the game
                self.restart()
            else:

                # End the game
                return

        # Determine whose turn it is
        if self.turn == "player":

            # Handle player's turn
            self.do_player_turn()
        elif self.turn == "computer":

            # Handle computer's turn
            self.do_computer_turn()
        else:

            # Throw error if the turn value is unknown
            raise ValueError("Unknown turn value.")

        # Add newlines.
        print("\n\n\n")


def play_a_new_game():
    # Initialize a game instance
    game = TicTacToe()

    # While the game has not ended
    while not game.end:
        # play the game
        game.play_turn()


if __name__ == '__main__':
    # Run the game loop
    play_a_new_game()
