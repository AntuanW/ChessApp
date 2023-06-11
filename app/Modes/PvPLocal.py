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
                moveMade = handle_player_move(sqSelected, playerClicks, simulation, screen)

            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    p.quit()
                    running = False
                    from app.GUI.ModeWindow.ModeWindow import ModeWindow
                    ModeWindow().run()

        if moveMade:
            running = draw_game(screen, simulation, None, game_mode)
            moveMade = False
