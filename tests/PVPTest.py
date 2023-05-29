from app.Modes import PvPLocal
from saves import saves
import chess

save = saves[5]

if __name__ == "__main__":
    PvPLocal.game(save)


