from app.Enums.modeEnum import GameMode
from app.Modes.Ultis import *


def game(player_colour=chess.WHITE, difficulty=2, save=None):

    game_mode = GameMode.PLAYER_VS_COMPUTER
    screen, clock = init_screen()

    simulation, starting_move_number = make_computer_game(
        difficulty, save, player_colour)

    running, moveMade = True, False
    sqSelected = []
    playerClicks = []

    if is_computer_starting(player_colour, simulation) and simulation.isGameRunning():
        simulation.makeComputerMove()

    running = draw_game(screen, simulation, player_colour, game_mode)

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and simulation.isGameRunning():
                moveMade = handle_player_move(sqSelected, playerClicks, simulation)

            elif e.type == p.KEYDOWN and simulation.isGameRunning():
                handle_undo(simulation, starting_move_number, sqSelected, playerClicks)
                running = draw_game(screen, simulation, player_colour, game_mode)

        if moveMade:
            running = draw_game(screen, simulation, player_colour, game_mode)

            if simulation.isGameRunning():
                simulation.makeComputerMove()
                running = draw_game(screen, simulation, player_colour, game_mode)
                moveMade = False
