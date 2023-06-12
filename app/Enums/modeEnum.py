from enum import Enum


class GameMode(Enum):
    PLAYER_VS_COMPUTER = "Player VS Computer"
    PLAYER_VS_PLAYER_LOCAL = "Player VS Player (Local)"
    PLAYER_VS_PLAYER_ONLINE = "Player VS Player (Online)"


def get_key_by_value(value):
    for key, enum_value in GameMode.__members__.items():
        if enum_value.value == value:
            return key
