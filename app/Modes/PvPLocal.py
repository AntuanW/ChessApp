import chess

from app import GameEngine
from app.GUI.Draw import *


def game(save=None):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    load_images()

    if save is None:
        simulation = GameEngine.GameState()
    else:
        simulation = GameEngine.GameState(game_save=save)

    running = True
    sqSelected = ()
    playerClicks = []
    moveMade = False
    gameStatus = simulation.isGameRunning()

    draw_game_state(screen, simulation)
    clock.tick(MAX_FPS)
    p.display.flip()

    if not gameStatus:
        draw_end_screen(screen, simulation.getGameStatus())
        running = False

    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and gameStatus:

                location = p.mouse.get_pos()

                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE

                if sqSelected == (row, col):

                    sqSelected = ()
                    playerClicks = []

                else:

                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                    # draw circles for legal moves
                    # detect_legal_moves_and_draw_circles(sqSelected, screen, simulation.board)

                if len(playerClicks) == 2:

                    start_row, start_col = playerClicks[0][0], playerClicks[0][1]
                    end_row, end_col = playerClicks[1][0], playerClicks[1][1]

                    start_move = colsToRanks[start_col] + rowsToRanks[start_row]
                    end_move = colsToRanks[end_col] + rowsToRanks[end_row]

                    action = chess.Move.from_uci(start_move + end_move)

                    if action in simulation.board.legal_moves:
                        sqSelected = ()
                        playerClicks = []

                        simulation.makePlayerMove(action)
                        moveMade = True
                        break
                    else:
                        print("illegal")
                        sqSelected = ()
                        playerClicks = []

        if moveMade:
            draw_game_state(screen, simulation)
            gameStatus = simulation.isGameRunning()
            if not gameStatus:
                draw_end_screen(screen, simulation.getGameStatus())
                clock.tick(MAX_FPS)

            clock.tick(MAX_FPS)
            p.display.flip()

            moveMade = False
