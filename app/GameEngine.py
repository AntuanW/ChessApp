import chess

from app.ChessEngine import ChessEngine


class GameState:
    def __init__(self, game_save=None, difficulty=1):
        if game_save is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(game_save)

        self.engine = ChessEngine(self.board, difficulty)

    def makePlayerMove(self, move):
        self.engine.make_move(move)

    def makeComputerMove(self):
        self.engine.make_best_move()

    def isGameRunning(self):
        if self.board.outcome() is not None:
            return False
        else:
            return True

    def getGameStatus(self):
        return self.board.outcome()
