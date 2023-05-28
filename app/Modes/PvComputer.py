import chess

from app import GameEngine
from app.GUI.Draw import *

def game(player_colour=chess.WHITE, dificulty=2, save=None):

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    load_images()

    if save is None:
        simulation = GameEngine.GameState(depth=dificulty)
        starting_move_number = 1
    else:
        simulation = GameEngine.GameState(game_save=save, depth=dificulty)
        starting_move_number = int(save[len(save)-1])
        if player_colour==chess.WHITE and simulation.board.turn==chess.BLACK: starting_move_number += 1


    running = True
    sqSelected = ()
    playerClicks = []
    moveMade = False
    gameStatus = simulation.isGameRunning()
    if not gameStatus:
        draw_end_screen(screen, simulation.getGameStatus())
        clock.tick(MAX_FPS)

    if (player_colour == chess.BLACK and simulation.board.turn == True) or (player_colour == chess.WHITE and simulation.board.turn == False):
        simulation.makeComputerMove()
        gameStatus = simulation.isGameRunning()
        if not gameStatus:
            draw_end_screen(screen, simulation.getGameStatus())
            clock.tick(MAX_FPS)

    draw_game_state(screen, simulation)
    clock.tick(MAX_FPS)
    p.display.flip()

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

                # if len(playerClicks) == 1:

                    # draw circles for legal moves
                    # draw_circle(4, 2, screen)/
                    # draw_board(screen)
                    # draw_pieces(screen, simulation.board)
                    # print("working")
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
                    else:
                        print("illegal")
                        sqSelected = ()
                        playerClicks = []


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and simulation.board.fullmove_number - starting_move_number >= 1:
                    simulation.engine.unmake_move()
                    simulation.engine.unmake_move()
                    sqSelected = ()
                    playerClicks = []

                    draw_game_state(screen, simulation)
                    clock.tick(MAX_FPS)
                    p.display.flip()

        if moveMade:
            draw_game_state(screen, simulation)
            clock.tick(MAX_FPS)
            p.display.flip()

            gameStatus = simulation.isGameRunning()
            if not gameStatus:
                if not gameStatus:
                    draw_end_screen(screen, simulation.getGameStatus())
                    clock.tick(MAX_FPS)

            simulation.makeComputerMove()
            draw_game_state(screen, simulation)
            clock.tick(MAX_FPS)
            p.display.flip()
            moveMade = False

            gameStatus = simulation.isGameRunning()
            if not gameStatus:
                if not gameStatus:
                    draw_end_screen(screen, simulation.getGameStatus())
                    clock.tick(MAX_FPS)


# game(chess.WHITE)