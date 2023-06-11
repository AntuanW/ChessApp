import time

import chess
from app import GameEngine
from app.GUI.Draw import *
from app.GUI.ModeWindow.EndgameWindow import EndgameWindow
from app.config import get_username
import requests
from app.Enums import modeEnum


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


def draw_game(screen, simulation: GameEngine.GameState, player_color, game_mode):
    p.display.set_caption(give_info(simulation.board.turn, game_mode))
    if not simulation.isGameRunning():
        draw_game_state(screen, simulation)
        p.display.flip()
        time.sleep(3)
        return EndgameWindow(player_color, simulation.board.fen(), simulation.board.outcome(),
                             simulation.engine.difficulty, game_mode).run()
    else:
        draw_game_state(screen, simulation)
        p.display.flip()
        return True


def give_info(turn, mode: modeEnum.GameMode):
    res = "To move: "
    if turn:
        res += "WHITE, "
    else:
        res += "BLACK, "
    res += "controls: Q - quit,"
    if mode == modeEnum.GameMode.PLAYER_VS_COMPUTER:
        res += " S - save, Z - undo"

    return res


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


def handle_player_move(sqSelected: list, playerClicks: list, simulation: GameEngine.GameState, screen):
    handle_mouse_buttons(sqSelected, playerClicks)

    if len(playerClicks) == 1:
        if can_be_clicked(make_selected_str(playerClicks), simulation.board):
            print("[CONSOLE] Selected:", make_selected_str(playerClicks))
            draw_possible_moves(screen, simulation, make_selected_str(playerClicks))
        else:
            reset_move_arrays(sqSelected, playerClicks)

    elif len(playerClicks) == 2:
        action = chess.Move.from_uci(make_move_str(playerClicks))
        if action in simulation.board.legal_moves:
            reset_move_arrays(sqSelected, playerClicks)
            simulation.makePlayerMove(action)
            print("[CONSOLE] Move made: ", action)
            return True
        action.promotion = chess.QUEEN  # fake promotion
        if action in simulation.board.legal_moves:
            reset_move_arrays(sqSelected, playerClicks)
            action.promotion = promotion_prompt()
            simulation.makePlayerMove(action)
            print("[CONSOLE] Move made: ", action)
            return True
        else:
            reset_move_arrays(sqSelected, playerClicks)
            print("[CONSOLE] ILLEGAL MOVE")
            return False


def promotion_prompt():
    # todo promotion gui
    print("[CONSOLE] Select piece:")
    print("1 -> Queen")
    print("2 -> Bishop")
    print("3 -> Rook")
    print("4 -> Knight")
    while True:
        prom = input("Selected piece:")
        match prom:
            case '1':
                return chess.QUEEN
            case '2':
                return chess.BISHOP
            case '3':
                return chess.ROOK
            case '4':
                return chess.KNIGHT
            case _:
                print("[CONSOLE] INVALID NUMBER")


def can_be_clicked(str_square: str, board: chess.Board):
    square = chess.parse_square(str_square)

    if board.color_at(square) is not board.turn:
        return False
    else:
        possible_starts = set(map(lambda x: x.uci()[:2], board.legal_moves))
        if str_square in possible_starts:
            return True
        else:
            return False


def handle_save(simulation: GameEngine.GameState):
    save_game(simulation.board.fen(), simulation.engine.difficulty)


def save_game(game_state, difficulty):
    data = {
        "username": get_username(),
        "game_state": game_state,
        "difficulty": difficulty
    }

    try:
        print("saving game state to database...")
        response = requests.put("http://localhost:8080/save_game", json=data)
        if response.status_code == 200:
            print("game state successfully saved to the database")
        else:
            print("Failed to save game state to the database. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", str(e))
