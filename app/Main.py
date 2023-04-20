import GameEngine
from GUI.Draw import *

def main():

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    load_images()

    simulation = GameEngine.GameState()

    running = True
    sqSelected = ()
    playerClicks = []
    moveMade = False

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

                    # legal moves drawing


                if len(playerClicks) == 2:

                    start_row, start_col = playerClicks[0][0], playerClicks[0][1]
                    end_row, end_col = playerClicks[1][0], playerClicks[1][1]

                    start_move = colsToRanks[start_col] + rowsToRanks[start_row]
                    end_move = colsToRanks[end_col] + rowsToRanks[end_row]

                    action = start_move + end_move
                    # print(action)

                    for legal_move in simulation.board.legal_moves:

                        if legal_move.uci() == action:

                            sqSelected = ()
                            playerClicks = []

                            simulation.makePlayerMove(action)
                            moveMade = True

                            break
                    else:
                        print("illegal")
                        sqSelected = ()
                        playerClicks = []

                    pass

            # elif e.type == p.KEYDOWN:
            #     if e.key == p.K_z:
            #         pass

        draw_game_state(screen, simulation)

        clock.tick(MAX_FPS)
        p.display.flip()

        if moveMade:

            simulation.makeComputerMove()
            moveMade = False

if __name__ == "__main__":
    main()
