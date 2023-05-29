from app.Modes.Ultis import *


def game(player_colour=chess.WHITE, difficulty=2, save=None):
    screen, clock = init_screen()

    simulation, starting_move_number = make_computer_game(
        difficulty, save, player_colour)

    running, moveMade = True, False
    sqSelected = []
    playerClicks = []

    running = draw_game(screen, simulation, player_colour)

    if is_computer_starting(player_colour, simulation) and simulation.isGameRunning():
        simulation.makeComputerMove()

    running = draw_game(screen, simulation, player_colour)

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and simulation.isGameRunning():
                moveMade = handle_player_move(sqSelected, playerClicks, simulation)

            elif e.type == p.KEYDOWN and simulation.isGameRunning():
                handle_undo(simulation, starting_move_number, sqSelected, playerClicks)
                running = draw_game(screen, simulation, player_colour)

        if moveMade:
            running = draw_game(screen, simulation, player_colour)

            if simulation.isGameRunning():
                simulation.makeComputerMove()
                running = draw_game(screen, simulation, player_colour)
                moveMade = False
