#!/usr/bin/env python3

import argparse
import numpy as np
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
           'Q' : 0.011,
           'K' : 0.014,}

board = chess.Board()

def main():
    parser = argparse.ArgumentParser(description='Robot Chess Player for the WidowX-200')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
    print("Starting robot.")

    is_open = 1
    try:
        playing = True
        while playing:
            # Go home
            client.move(np.array([0.1, 0, 0.1, 0, 1.57, 0])) # Move home
            time.sleep(1)
            # print_yellow("Enter moves as [x y] where x is the index of the square the piece starts at, and y is the square the piece moves to.")
            print_yellow("Enter moves as their algebraic notation. For example, moving a Pawn from e2 to e4 would be <e4>, and moving a Knight from b1 to c3 is <Nc3> (without the <>)" )

            ## Player's move ##
            player_move = input("Enter when finished playing the move. White's move: ")
            # if len(player_move.split(" ")) != 2:
            #     print_yellow("Please enter two arguments.")
            #     continue
            # player_from_square = int(player_move.split(" ")[0])
            # player_to_square = int(player_move.split(" ")[1])
            # # Update the board with the player's move
            # board.push(move=chess.Move(from_square=player_from_square, to_square=player_to_square))
            board.push_san(player_move)


            print(board)
            ## Bot move ##
            # bot_move = input("Bot's move: ")
            # if len(bot_move.split(" ")) != 2:
            #     print_yellow("Please enter two arguments.")
            #     continue

            # bot_from_square = int(bot_move.split(" ")[0])
            # bot_to_square = int(bot_move.split(" ")[1])

            # client.move(np.array([0.15, 0, 0.15, 0, 1.57, 0])) # Move home
    
            # height = heights[bot_from_square], poses[bot_to_square], height, clearance_height, client)
            # # Update the board with the bot's move
            # board.push(move=chess.Move(from_squared.piece_at(bot_from_square).symbol().upper()]
            # print(board.piece_at(bot_from_square).symbol().upper())
            # clearance_height = height + 0.08
            # pick_and_place(poses[=bot_from_square, to_square=bot_to_square))
            
            # Get the move of the bot
            minmax = minimax.Minimax(board)
            score, bot_move = minmax.alpha_beta_min(
                5, float("-inf"), float("inf"), chess.Move.null()
            )
            
            # Play the move on the physical board

            bot_from_square, bot_to_square = (bot_move.from_square, bot_move.to_square)
            height = heights[board.piece_at(bot_from_square).symbol().upper()]

            if board.is_capture(bot_move):
                print_yellow("Capture!")
                ######### DAN ############
                print(f"Capturing on {bot_move.to_square}")
                pass

        
            clearance_height = height + 0.08
            pick_and_place(xy_initial=poses[bot_from_square], 
                           xy_final=poses[bot_to_square], 
                           height=height, 
                           clearance_height=clearance_height, 
                           client=client)

            # Update virtual board model
            board.push(bot_move)
            print(board)
            print_yellow("Move played.")




    except KeyboardInterrupt:
        time.sleep(1)
        client.reset()
        time.sleep(1)
        client.stop()
    

if __name__ == "__main__":
    main()
