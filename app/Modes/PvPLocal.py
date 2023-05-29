from app.Modes.Ultis import *


def game(save=None):
    screen, clock = init_screen()

    simulation = make_local_game(save)

    running, moveMade = True, False
    sqSelected = []
    playerClicks = []

    running = draw_game(screen, simulation, None)

    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and simulation.isGameRunning():
                moveMade = handle_player_move(sqSelected, playerClicks, simulation)

        if moveMade:
            running = draw_game(screen, simulation, None)
            moveMade = False
