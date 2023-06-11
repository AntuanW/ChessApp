import time
import pygame as p
import chess
import requests

from app import GameEngine
from app.GUI.Draw import *
from app.GUI.ModeWindow.EndgameWindow import EndgameWindow
from app.config import get_username
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
        else:
            reset_move_arrays(sqSelected, playerClicks)

    elif len(playerClicks) == 2:
        action = chess.Move.from_uci(make_move_str(playerClicks))
        if action in simulation.board.legal_moves:
            reset_move_arrays(sqSelected, playerClicks)
            simulation.makePlayerMove(action)
            print("[CONSOLE] Move made: ", action)
            return True
        action.promotion = chess.QUEEN
        if action in simulation.board.legal_moves:
            reset_move_arrays(sqSelected, playerClicks)
            action.promotion = promotion_window(screen, color="w")
            simulation.makePlayerMove(action)
            print("[CONSOLE] Move made: ", action)
            return True
        else:
            reset_move_arrays(sqSelected, playerClicks)
            print("[CONSOLE] ILLEGAL MOVE")
            return False

def promotion_window(screen, color):

    queen_image = p.transform.scale(p.image.load(f"../resources/ChessImg/{color}Q.png"), (60, 60))
    bishop_image = p.transform.scale(p.image.load(f"../resources/ChessImg/{color}B.png"), (60, 60))
    rook_image = p.transform.scale(p.image.load(f"../resources/ChessImg/{color}R.png"), (60, 60))
    knight_image = p.transform.scale(p.image.load(f"../resources/ChessImg/{color}N.png"), (60, 60))

    queen_button = p.Rect(50, 200, 70, 70)
    bishop_button = p.Rect(164, 200, 70, 70)
    rook_button = p.Rect(278, 200, 70, 70)
    knight_button = p.Rect(392, 200, 70, 70)

    running = True

    font1 = p.font.Font(None, 40)
    font2 = p.font.Font(None, 22)
    font3 = p.font.Font(None, 26)
    label1 = font1.render("You have been promoted!", True, (255, 255, 255))
    label2 = font2.render("Choose a piece that you want to obtain upon promotion of a pawn:", True, (255, 255, 255))
    queen_label = font3.render("Queen", True, (255, 255, 255))
    bishop_label = font3.render("Bishop", True, (255, 255, 255))
    rook_label = font3.render(" Rook", True, (255, 255, 255))
    knight_label = font3.render("Knight", True, (255, 255, 255))

    button_color = (155, 155, 155)
    button_hover_color = (120, 120, 120)

    queen_hovered = False
    bishop_hovered = False
    rook_hovered = False
    knight_hovered = False

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                if queen_button.collidepoint(mouse_pos):
                    return chess.QUEEN
                elif bishop_button.collidepoint(mouse_pos):
                    return chess.BISHOP
                elif rook_button.collidepoint(mouse_pos):
                    return chess.ROOK
                elif knight_button.collidepoint(mouse_pos):
                    return chess.KNIGHT

        screen.fill((0, 0, 0))

        screen.blit(label1, (88, 100))
        screen.blit(label2, (20, 150))

        queen_hovered = queen_button.collidepoint(p.mouse.get_pos())
        bishop_hovered = bishop_button.collidepoint(p.mouse.get_pos())
        rook_hovered = rook_button.collidepoint(p.mouse.get_pos())
        knight_hovered = knight_button.collidepoint(p.mouse.get_pos())

        queen_button_color = button_hover_color if queen_hovered else button_color
        bishop_button_color = button_hover_color if bishop_hovered else button_color
        rook_button_color = button_hover_color if rook_hovered else button_color
        knight_button_color = button_hover_color if knight_hovered else button_color

        p.draw.rect(screen, queen_button_color, queen_button)
        screen.blit(queen_image, (queen_button.x + 5, queen_button.y + 5))
        queen_label_rect = queen_label.get_rect(centerx=queen_button.centerx, top=queen_button.bottom + 10)
        screen.blit(queen_label, queen_label_rect)

        p.draw.rect(screen, bishop_button_color, bishop_button)
        screen.blit(bishop_image, (bishop_button.x + 5, bishop_button.y + 5))
        bishop_label_rect = bishop_label.get_rect(centerx=bishop_button.centerx, top=bishop_button.bottom + 10)
        screen.blit(bishop_label, bishop_label_rect)

        p.draw.rect(screen, rook_button_color, rook_button)
        screen.blit(rook_image, (rook_button.x + 5, rook_button.y + 5))
        rook_label_rect = rook_label.get_rect(centerx=rook_button.centerx, top=rook_button.bottom + 10)
        screen.blit(rook_label, rook_label_rect)

        p.draw.rect(screen, knight_button_color, knight_button)
        screen.blit(knight_image, (knight_button.x + 5, knight_button.y + 5))
        knight_label_rect = knight_label.get_rect(centerx=knight_button.centerx, top=knight_button.bottom + 10)
        screen.blit(knight_label, knight_label_rect)

        p.display.flip()

    p.quit()



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
