from app.Enums.modeEnum import GameMode
from app.Modes.Ultis import *
from app.config import MAX_FRAMERATE


def game(player_colour=chess.WHITE, difficulty=2, save=None):
    game_mode = GameMode.PLAYER_VS_COMPUTER
    screen, clock = init_screen()

    simulation, starting_move_number = make_computer_game(
        difficulty, save, player_colour)

    running, move_made = True, False
    square_selected = []
    player_clicks = []

    if is_computer_starting(player_colour, simulation) and simulation.is_game_running():
        simulation.make_computer_move()

    running = draw_game(screen, simulation, player_colour, game_mode)
    clock.tick(MAX_FRAMERATE)

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and simulation.is_game_running():
                move_made = handle_player_move(square_selected, player_clicks, simulation, screen)
                clock.tick(MAX_FRAMERATE)

            elif e.type == p.KEYDOWN and simulation.is_game_running():
                if e.key == p.K_z:
                    handle_undo(simulation, starting_move_number, square_selected, player_clicks)
                    running = draw_game(screen, simulation, player_colour, game_mode)
                    clock.tick(MAX_FRAMERATE)
                elif e.key == p.K_s:
                    handle_save(simulation)
                    p.quit()
                    running = False
                    from app.GUI.ModeWindow.PVC import PVC
                    PVC().run()
                elif e.key == p.K_q:
                    p.quit()
                    running = False
                    from app.GUI.ModeWindow.ModeWindow import ModeWindow
                    ModeWindow().run()

        if move_made:
            running = draw_game(screen, simulation, player_colour, game_mode)
            clock.tick(MAX_FRAMERATE)

            if simulation.is_game_running():
                simulation.make_computer_move()
                running = draw_game(screen, simulation, player_colour, game_mode)
                clock.tick(MAX_FRAMERATE)
                move_made = False
