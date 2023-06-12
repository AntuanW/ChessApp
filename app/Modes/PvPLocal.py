from app.Enums.modeEnum import GameMode
from app.Modes.Ultis import *
from app.config import MAX_FRAMERATE


def game(save=None):
    screen, clock = init_screen()
    game_mode = GameMode.PLAYER_VS_PLAYER_LOCAL
    simulation = make_local_game(save)

    running, move_made = True, False
    square_selected = []
    player_clicks = []

    running = draw_game(screen, simulation, None, game_mode)
    clock.tick(MAX_FRAMERATE)

    while running:

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and simulation.is_game_running():
                move_made = handle_player_move(square_selected, player_clicks, simulation, screen)
                clock.tick(MAX_FRAMERATE)

            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    p.quit()
                    running = False
                    from app.GUI.ModeWindow.ModeWindow import ModeWindow
                    ModeWindow().run()

        if move_made:
            running = draw_game(screen, simulation, None, game_mode)
            clock.tick(MAX_FRAMERATE)
            move_made = False
