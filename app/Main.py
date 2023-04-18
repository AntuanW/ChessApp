import chess
import pygame as p
import GameEngine

# GLOBAL VARIABLES
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
colsToRanks = {v: k for k, v in filesToCols.items()}

def load_images():
    pieces = ["p", "r", "n", "b", "q", "k", "P", "R", "N", "B", "Q", "K"]
    for piece in pieces:
        if piece.islower():
            IMAGES[piece] = p.transform.scale(p.image.load("../resources/b" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        else:
            IMAGES[piece] = p.transform.scale(p.image.load("../resources/w" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
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

def main():

    # INITIAL GAME WINDOW
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    load_images()

    simulation = GameEngine.GameState()


    running = True
    sqSelected = ()
    playerClicks = []

    while running:

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:

                location = p.mouse.get_pos()

                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:

                    # print(playerClicks)
                    # print(simulation.board.legal_moves)

                    start_row, start_col = playerClicks[0][0], playerClicks[0][1]
                    end_row, end_col = playerClicks[1][0], playerClicks[1][1]

                    start_move = colsToRanks[start_col] + rowsToRanks[start_row]
                    end_move = colsToRanks[end_col] + rowsToRanks[end_row]

                    action = start_move + end_move
                    # print(action)

                    for legal_move in simulation.board.legal_moves: # zmienic

                        if legal_move.uci() == action:

                            sqSelected = ()
                            playerClicks = []

                            simulation.makeMove(action)

                            break
                    else:
                        print("illegal")
                        sqSelected = ()
                        playerClicks = []

                    pass

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    pass

        draw_game_state(screen, simulation)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
