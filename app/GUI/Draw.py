import pygame as p
import chess


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
            IMAGES[piece] = p.transform.scale(p.image.load("../resources/ChessImg/b" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        else:
            IMAGES[piece] = p.transform.scale(p.image.load("../resources/ChessImg/w" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


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

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def detect_legal_moves_and_draw_circles(sqSelected, screen, board):

    start_row = sqSelected[0]
    start_col = sqSelected[1]

    piece = convert(start_row, start_col, board)

    if piece != None:

        uci_move = get_uci_move(sqSelected)

        print(uci_move)

        for legal_move in board.legal_moves:

            legal_start_move = legal_move.uci()[0:2]

            end_col = filesToCols[legal_move.uci()[2]]
            end_row = ranksToRows[legal_move.uci()[3]]

            if legal_start_move == uci_move:
                print(legal_move)
                draw_circle(end_row, end_col, screen)

    return True


def draw_circle(row, column, screen):

    center_x = column * SQ_SIZE + SQ_SIZE // 2
    center_y = row * SQ_SIZE + SQ_SIZE // 2

    radius = SQ_SIZE // 5

    p.draw.circle(screen, LIGHT_GRAY_WITH_OPACITY, (center_x, center_y), radius)




def draw_end_screen(screen, outcome):

    screen.fill(WHITE)
    p.display.set_caption("GAME OVER!")

    font = p.font.Font(None, 52)

    game_over_text = font.render("Game Over due to:", True, BLACK)
    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 100))

    result_text = font.render(outcome.termination.name, True, BLACK)
    result_text_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    if outcome.winner is True:
        winner_color = "White"
    elif outcome.winner is False:
        winner_color = "Black"
    else:
        winner_color = "None"

    winner_text = font.render("Winner: " + winner_color, True, BLACK)
    winner_text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 100))

    screen.blit(game_over_text, game_over_text_rect)

    screen.blit(result_text, result_text_rect)

    screen.blit(winner_text, winner_text_rect)

    p.display.flip()
