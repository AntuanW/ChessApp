import chess
from app.Modes import PvComputer

saves = [
"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",   #0 czarne na ruchu
"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2", #1 białe na ruchu
"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2", #2 białe na ruchu
"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",   #3 czarne na ruchu
"4k3/8/8/8/1Q5B/8/8/4K3 w - - 0 1",                             #4 białe na ruchu, mat w 1
]
save = saves[4]
our_color = chess.BLACK
difficulty = 1

if __name__ == '__main__':
    PvComputer.game(our_color, difficulty, save)