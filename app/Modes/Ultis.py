import pygame.time

from app import GameEngine
from app.GUI.Draw import *


def init_screen():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    load_images()
    return screen, clock


def make_computer_game(difficulty, save, player_colour):
    if save is None:
        simulation = GameEngine.GameState(difficulty=difficulty)
        starting_move_number = 1
    else:
        simulation = GameEngine.GameState(game_save=save, difficulty=difficulty)
        starting_move_number = int(save[len(save) - 1])
        if player_colour == chess.WHITE and simulation.board.turn == chess.BLACK:
            starting_move_number += 1
    return simulation, starting_move_number


def make_local_game(save):
    if save is None:
        return GameEngine.GameState()
    else:
        return GameEngine.GameState(save)


def draw_game(screen, simulation: GameEngine.GameState, clock: pygame.time.Clock):
    if not simulation.isGameRunning():
        draw_end_screen(screen, simulation.getGameStatus())
        clock.tick(MAX_FPS)
    else:
        draw_game_state(screen, simulation)
    p.display.flip()


def is_computer_starting(player_colour: chess.Color, simulation: GameEngine.GameState):
    return (
            player_colour == chess.BLACK and simulation.board.turn
    ) or (
            player_colour == chess.WHITE and not simulation.board.turn
    )


def handle_mouse_buttons(sqSelected: list, playerClicks: list):
    location = p.mouse.get_pos()

    row = location[1] // SQ_SIZE
    col = location[0] // SQ_SIZE

    if sqSelected == [row, col]:
        reset_move_arrays(sqSelected, playerClicks)
        print("[CONSOLE] RESET CLICKS")
    else:
        sqSelected.append(row)
        sqSelected.append(col)
        playerClicks.append([row, col])


def make_selected_str(playerClicks: list):
    start_row, start_col = playerClicks[0][0], playerClicks[0][1]
    return colsToRanks[start_col] + rowsToRanks[start_row]


def make_move_str(playerClicks: list):
    end_row, end_col = playerClicks[1][0], playerClicks[1][1]
    end_move = colsToRanks[end_col] + rowsToRanks[end_row]
    return make_selected_str(playerClicks) + end_move


def reset_move_arrays(sqSelected: list, playerClicks: list):
    sqSelected.clear()
    playerClicks.clear()


def handle_undo(simulation: GameEngine.GameState, starting_move_number: int, sqSelected: list, playerClicks: list):
    if simulation.board.fullmove_number - starting_move_number >= 1:
        simulation.engine.unmake_move()
        simulation.engine.unmake_move()
        reset_move_arrays(sqSelected, playerClicks)


def handle_player_move(sqSelected: list, playerClicks: list, simulation: GameEngine.GameState):
    handle_mouse_buttons(sqSelected, playerClicks)

    if len(playerClicks) == 1:
        print("[CONSOLE] Selected:", make_selected_str(playerClicks))

    elif len(playerClicks) == 2:
        action = chess.Move.from_uci(make_move_str(playerClicks))
        if action in simulation.board.legal_moves:
            reset_move_arrays(sqSelected, playerClicks)
            simulation.makePlayerMove(action)
            print("[CONSOLE] Move made: ", action)
            return True
        else:
            reset_move_arrays(sqSelected, playerClicks)
            print("[CONSOLE] ILLEGAL MOVE")
            return False
