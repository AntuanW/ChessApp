import chess
import ChessEngine
from enum import Enum

class GameType(Enum):
    LOCAL = 0  # 1vs1 on the same device
    MULTIPLAYER = 1  # 1vs1 online
    SINGLEPLAYER = 2  # 1vs engine

class GameState:
    def __init__(self, game_save=None, game_type=GameType.LOCAL):
        if game_save is None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(game_save)

        self.engine = ChessEngine.ChessEngine()
        self.game_type = game_type


    def makePlayerMove(self, action):

        move = chess.Move.from_uci(action)
        self.board.push(move)

    def makeComputerMove(self):

        self.engine.make_best_move(self.board)

