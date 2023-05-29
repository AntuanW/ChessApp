from app.Modes import PvPLocal
from saves import saves


save = saves[4]

if __name__ == "__main__":
    PvPLocal.game(save)