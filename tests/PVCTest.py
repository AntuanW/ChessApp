import chess

from app.Modes import PvComputer
from saves import saves

save = saves[4]
our_color = chess.BLACK
difficulty = 1

if __name__ == '__main__':
    PvComputer.game(our_color, difficulty, save)
