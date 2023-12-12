import random
import math
from copy import copy, deepcopy

MAX_DEPTH = 2

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def is_drop_phase(self, state):
        count = 0
        for i in range (5):
            for j in range(5):
                if state[i][j] != ' ':
                    count += 1
        return count < 8

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = self.is_drop_phase(state)   # TODO: detect drop phase

        max = -1
        candidate = None
        succ = self.succ(state)
        # print("succ: "+ str(succ))
        for s in succ:
            if self.max_value(s, 0) > max:
                candidate = s
        # print('candidate: ' + str(candidate))

        move = []
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            for i in range(5):
                for j in range(5):
                    if candidate[i][j] == ' ' and state[i][j] != ' ':
                        move.insert(0, (i, j))
                        break

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better

        for i in range(5):
            for j in range(5):
                if state[i][j] == ' ' and candidate[i][j] != ' ':
                    move.insert(0, (i, j))
                    break
        
        # print(move)
        return move
    
    def max_value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        elif depth == MAX_DEPTH:
            return self.heuristic_game_value(state)
        elif depth %2 == 0:
            # MAX's move
            succ = self.succ(state)
            return max(self.max_value(next_state, depth+1) for next_state in succ)
        else:
            # MIN's move
            succ = self.succ(state)
            return min(self.max_value(next_state, depth+1) for next_state in succ)
    

    
    def succ(self, state):
        # print("tryna get succ of state: " + str(state))
        drop_phase = self.is_drop_phase(state)
        succ_list = []
        if drop_phase:
            for i in range (5):
                for j in range(5):
                    if state[i][j] == ' ':
                        candidate = deepcopy(state)
                        candidate[i][j] = self.my_piece
                        succ_list.append(candidate)
        else:
            for i in range (5):
                for j in range(5):
                    if state[i][j] == self.my_piece:
                        for l in {0, 1, -1}:
                            for k in {0, 1, -1}:
                                if l == 0 and k == 0:
                                    continue
                                x = i+l
                                y = j+k
                                if x in range(0, 5) and y in range(0, 5) and state[x][y] == ' ':
                                    candidate = deepcopy(state)
                                    candidate[i][j] = ' '
                                    candidate[x][y] = self.my_piece
                                    succ_list.append(candidate)

        return succ_list

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        for i in range(2):
            for j in range(3, 5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    return 1 if state[i][j] == self.my_piece else -1

        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j] == state[i][j+1] == state[i+1][j+1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0 # no winner yet
    

    # Function to calculate minimum additional tokens required for a win condition
    def min_moves_to_win(self, state, piece):
        def count_pieces(line, piece):
            return sum(1 for cell in line if cell == piece)

        min_moves = 4  # Maximum 4 moves required to win

        # Check rows and columns
        for i in range(5):
            row_pieces = count_pieces(state[i], piece)
            col_pieces = count_pieces([state[j][i] for j in range(5)], piece)
            min_moves = min(min_moves, 4 - row_pieces, 4 - col_pieces)

        # Check diagonals
        for i in range(2):
            for j in range(2):
                diag1 = [state[x+i][x+j] for x in range(4)]
                diag2 = [state[x+i][3-x+j] for x in range(4)]
                diag1_pieces = count_pieces(diag1, piece)
                diag2_pieces = count_pieces(diag2, piece)
                min_moves = min(min_moves, 4 - diag1_pieces, 4 - diag2_pieces)

        # Check 2x2 squares
        for i in range(4):
            for j in range(4):
                square = [state[i][j], state[i+1][j], state[i][j+1], state[i+1][j+1]]
                square_pieces = count_pieces(square, piece)
                min_moves = min(min_moves, 4 - square_pieces)

        return min_moves
    
    def heuristic_game_value(self, state):
        # First, check if the game has a definite winner
        game_val = self.game_value(state)
        if game_val != 0:
            return float(game_val)

        min_moves_my_piece = self.min_moves_to_win(state, self.my_piece)
        min_moves_opp_piece = self.min_moves_to_win(state, self.opp)

        # Calculate the difference in moves to win
        move_diff = min_moves_opp_piece - min_moves_my_piece

        # Normalize the difference to a float between -1 and 1
        # Adjust the normalization factor as needed based on the game's typical move counts
        normalization_factor = max(min_moves_my_piece, min_moves_opp_piece, 1)
        heuristic_value = move_diff / normalization_factor

        # Ensure the value is within the bounds of -1 to 1
        heuristic_value = max(min(heuristic_value, 1), -1)

        return heuristic_value


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
