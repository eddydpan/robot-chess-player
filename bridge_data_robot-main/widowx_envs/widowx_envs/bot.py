#!/usr/bin/env python3

import argparse
import numpy as np
import threading
import cv2
import time
import chess
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus
from widowx_envs.pick_and_place import pick_and_place
import sys
import os
# Add the 'chess-ai' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../chess-ai')))
import minimax
# from widowx_envs.cv import BoardView
from widowx_envs.cv import BoardView
import inspect

print_yellow = lambda x: print("\033[93m {}\033[00m" .format(x))

A1 = (0.45, -0.15)  # xy of A1 tile which is the 0th index in python-chess
initial_tile = A1
poses = [] # each index represents a tile from a1 to h8

# Populate poses list
for file in range(8):
    file_step = file * 0.0444 # 0.0434
    for rank in range(8):
        rank_step = rank * 0.0434
        poses.append((initial_tile[0] - file_step, initial_tile[1] + rank_step))

# Height dictionary
heights = {'P' : 0.004,
           'N' : 0.000,
           'B' : 0.006,
           'R' : 0.005,
           'Q' : 0.025,
           'K' : 0.032,}

board = chess.Board()



def main():
    captures = 0
    parser = argparse.ArgumentParser(description='Robot Chess Player for the WidowX-200')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
    print("Starting robot.")

    board_view = BoardView()

    is_open = 1
    try:
        playing = True
        client.move(np.array([0.1, 0, 0.15, 0, 1.5, 0]),blocking=True)
        while playing:
            post_capture = False
            # view_thread = threading.Thread(target = board_view.show_frame)
            # view_thread.start()

            # Go home
            # client.move(np.array([0.1, 0, 0.1, 0, 1.57, 0])) # Move home
            input("enter when arm is ready")


            board_view.locate_board(True)
            board_view.update_board_state()

            
            time.sleep(1)
            
            legal_moves_lst = [
                board.san(move)
                for move in board.legal_moves
            ]
            print(f"Availabe Moves: {legal_moves_lst}")

            # print_yellow("Enter moves as [x y] where x is the index of the square the piece starts at, and y is the square the piece moves to.")
            print_yellow("Enter moves as their algebraic notation. For example, moving a Pawn from e2 to e4 would be <e4>, and moving a Knight from b1 to c3 is <Nc3> (without the <>)" )

            valid_input = False
            # while not valid_input:
            ## Player's move ##
            input("Enter when finished playing the move. White's move: ")
            
            # move validation - use when running without camera
            # not yet integrated with CV move detection
            '''if player_move in legal_moves_lst:
                print_yellow("Move Accepted")
                valid_input = True
            else:
                print("Invalid move. Please input legal move.")'''

            # if len(player_move.split(" ")) != 2:
            #     print_yellow("Please enter two arguments.")
            #     continue
            # player_from_square = int(player_move.split(" ")[0])
            # player_to_square = int(player_move.split(" ")[1])
            # # Update the board with the player's move
            # board.push(move=chess.Move(from_square=player_from_square, to_square=player_to_square))


            # determine player move based on camera feed
            time.sleep(2)

            cell1, cell2 = board_view.find_moved_piece()

            print(cell1, cell2)

            piece1 = board.piece_at(chess.parse_square(cell1))
            piece2 = board.piece_at(chess.parse_square(cell2))

            print(piece1)
            print(piece2)

           #  print(piece1.color)

            if piece1 and piece1.color == chess.WHITE:
                piece = piece1
                player_from_square = chess.parse_square(cell1)
                player_to_square = chess.parse_square(cell2)
            else:
                player_from_square = chess.parse_square(cell2)
                piece = piece2
                player_to_square = chess.parse_square(cell1)
            
    
            board.push(chess.Move(player_from_square, player_to_square))

            print(board)
            
            # Get the move of the bot
            minmax = minimax.Minimax(board)
            score, bot_move = minmax.alpha_beta_min(
                5, float("-inf"), float("inf"), chess.Move.null()
            )
            
            # Play the move on the physical board

            bot_from_square, bot_to_square = (bot_move.from_square, bot_move.to_square)
            # print(poses[bot_from_square])
            # print(poses[bot_to_square])
            height = heights[board.piece_at(bot_from_square).symbol().upper()]

            if board.is_capture(bot_move):
                print_yellow("Capture!")
                

                height = heights[board.piece_at(bot_to_square).symbol().upper()]
                clearance_height = height + 0.1

                captures_per_row = 3
                offset = 0.05

                x_position = 0.18 + (captures // captures_per_row) * offset
                y_position = 0.2 + (captures % captures_per_row) * offset

                print(f"height: {height}")
                print(f"x_pos: {x_position}")
                print(f"y_pos: {y_position}")

                pick_and_place(xy_initial=poses[bot_to_square],
                            xy_final=(x_position, y_position),
                            height=height,
                            clearance_height=clearance_height, 
                            client=client)

                captures += 1
                print(f"Capturing on {bot_move.to_square}")
                post_capture = True

            height = heights[board.piece_at(bot_from_square).symbol().upper()]
            clearance_height = height + 0.1
            pick_and_place(xy_initial=poses[bot_from_square], 
                           xy_final=poses[bot_to_square], 
                           height=height, 
                           clearance_height=clearance_height, 
                           client=client,
                           post_capture=post_capture)

            # Update virtual board model
            board.push(bot_move)
            print(board)
            print_yellow("Move played.")

            if cv2.waitKey(1) == ord("q"):
                playing = False


        board_view.cap.release()
        cv2.destroyAllWindows

    except KeyboardInterrupt:
        time.sleep(1)
        client.reset()
        time.sleep(1)
        client.stop()
    

if __name__ == "__main__":
    main()
