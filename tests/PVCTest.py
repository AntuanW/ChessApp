import chess

from app.Modes import PvComputer
from saves import saves

save = saves[5]
our_color = chess.WHITE
difficulty = 1

if __name__ == '__main__':
    PvComputer.game(our_color, difficulty, save)
