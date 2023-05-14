import chess
import ChessEngine


class GameState:
    def __init__(self, game_save=None, depth=2):
        if game_save is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(game_save)

        self.engine = ChessEngine.ChessEngine(depth)

    def makePlayerMove(self, move):
        self.board.push(move)

    def makeComputerMove(self):

        self.engine.make_best_move(self.board)
