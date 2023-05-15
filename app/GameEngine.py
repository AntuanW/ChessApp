import chess
import ChessEngine

class GameState:
    def __init__(self, game_save=None, depth=2):
        if game_save is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(game_save)

        self.engine = ChessEngine.ChessEngine(self.board, depth)

    def makePlayerMove(self, move):
        self.engine.make_move(move)

    def makeComputerMove(self):
        self.engine.make_best_move()
