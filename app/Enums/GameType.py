from enum import Enum

class GameType(Enum):
    LOCAL = 0  # 1vs1 on the same device
    MULTIPLAYER = 1  # 1vs1 online
    SINGLEPLAYER = 2  # 1vs engine