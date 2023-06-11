import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

WHITE = p.Color("White")
BLACK = p.Color("Black")
GRAY = p.Color("Gray")
RED = p.Color("Red")
LIGHT_GRAY_WITH_OPACITY = p.Color(222, 222, 222, 100)

ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
colsToRanks = {v: k for k, v in filesToCols.items()}


def get_uci_move(sqSelected):
    start_row = sqSelected[0]
    start_col = sqSelected[1]

    return colsToRanks[start_col] + rowsToRanks[start_row]


def load_images():
    pieces = ["p", "r", "n", "b", "q", "k", "P", "R", "N", "B", "Q", "K"]
    for piece in pieces:
        if piece.islower():
            IMAGES[piece] = p.transform.scale(p.image.load("../resources/ChessImg/b" + piece + ".png"),
                                              (SQ_SIZE, SQ_SIZE))
        else:
            IMAGES[piece] = p.transform.scale(p.image.load("../resources/ChessImg/w" + piece + ".png"),
                                              (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    colors = [WHITE, GRAY]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def convert(r, c, board):
    return board.piece_at(r * 8 + c).__str__()


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = convert(r, c, board)
            if piece != "None":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, (DIMENSION - r - 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if r == 0:
                # Dodanie liter od "a" do "h" w pierwszym wierszu
                letter = chr(ord("a") + c)
                font = p.font.SysFont(None, 20)
                text = font.render(letter, True, p.Color("black"))
                screen.blit(text,
                            p.Rect(c * SQ_SIZE + 2, (DIMENSION - r - 1) * SQ_SIZE + SQ_SIZE - 18, SQ_SIZE, SQ_SIZE))
            if c == 0:
                # Dodanie cyfr od 1 do 8 w pierwszej kolumnie
                number = str(r + 1)
                font = p.font.SysFont(None, 20)
                text = font.render(number, True, p.Color("black"))
                screen.blit(text, p.Rect(c * SQ_SIZE + 2, (DIMENSION - r - 1) * SQ_SIZE + 2, SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)
    p.display.flip()


def draw_possible_moves(screen, gs, checked):
    detect_legal_moves_and_draw_legal_rect(checked, screen, gs.board)
    draw_pieces(screen, gs.board)

def detect_legal_moves_and_draw_legal_rect(uci_move, screen, board):

    draw_board(screen)

    for legal_move in board.legal_moves:

        legal_start_move = legal_move.uci()[0:2]

        end_col = filesToCols[legal_move.uci()[2]]
        end_row = ranksToRows[legal_move.uci()[3]]

        if legal_start_move == uci_move:
            draw_legal_rect(end_row, end_col, screen)

    draw_pieces(screen, board)
    p.display.flip()

    return True


def draw_legal_rect(row, column, screen):

    p.draw.rect(screen, "ORANGE", p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


