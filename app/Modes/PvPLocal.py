from app.Enums.modeEnum import GameMode
from app.Modes.Ultis import *


def game(save=None):

    screen, clock = init_screen()
    game_mode = GameMode.PLAYER_VS_PLAYER_LOCAL
    simulation = make_local_game(save)

    running, moveMade = True, False
    sqSelected = []
    playerClicks = []

    running = draw_game(screen, simulation, None, game_mode)

    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and simulation.isGameRunning():

                moveMade = handle_player_move(sqSelected, playerClicks, simulation)



        if moveMade:
            running = draw_game(screen, simulation, None, game_mode)
            moveMade = False
