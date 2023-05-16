import chess
from Modes import PvComputer, PvPLocal, PvPOnline
from app.GUI.Auth.LoginWindow import LoginWindow

if __name__ == "__main__":
    #PvComputer.game(chess.BLACK, 2, "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1") #gramy czarnymi i wczytujemy pozycje gdzie ruch jest czarnych
    #PvComputer.game(chess.BLACK, 2, "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2") #gramy czarnymi i wczytujemy pozycje gdzie ruch jest białych
    #PvComputer.game(chess.WHITE, 2, "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2") #gramy białymi i wczytujemy pozycje gdzie ruch jest białych
    #PvComputer.game(chess.WHITE, 2, "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1") #gramy białymi i wczytujemy pozycje gdzie ruch jest czarnych
    #PvComputer.game(chess.WHITE, 3) #gramy białymi
    #PvComputer.game(chess.BLACK, 3) #gramy czarnymi
    #PvPLocal.game() #PvP
    #PvPLocal.game("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1") #wczytana gra gdzie ruch maja czarne
    #PvPLocal.game("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2") #wczytana gra gdzie ruch maja białe
    #PvPLocal.game("4k3/8/8/8/1Q5B/8/8/4K3 w - - 0 1")
    #PvPLocal.game("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    pass
    LoginWindow().run()

