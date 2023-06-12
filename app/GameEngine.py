import chess

from app.ChessEngine import ChessEngine


class GameState:
    def __init__(self, game_save=None, difficulty=1):
        if game_save is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(game_save)

        self.engine = ChessEngine(self.board, difficulty)

    def make_player_move(self, move):
        self.engine.make_move(move)

    def make_computer_move(self):
        self.engine.make_best_move()

    def is_game_running(self):
        if self.board.outcome() is not None:
            return False
        else:
            return True

    def get_game_status(self):
        return self.board.outcome()
