#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import time
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus
print_yellow = lambda x: print("\033[93m {}\033[00m" .format(x))



def pick_and_place(xy_initial, xy_final, height, clearance_height, client):
    '''
    Pick up an object at a certain position  and place it at a different position.

    Args: 
        xy_initial: 2-item list containing xy position of object in robot coordinate frame
        xy_final: 2-item list containing xy position of destination in robot coordinate frame
        height: height of object
        clearance_height: height the object must be raised to ensure it doesn't hit any other objects
        client: the client used to control the robot
    '''
    x_initial = xy_initial[0]
    y_initial = xy_initial[1]
    x_final = xy_final[0]
    y_final = xy_initial[1]

    # client.move(np.array([0.3, 0, 0.15, 0, 1.57, 0])) # Move home
    # time.sleep(2)
    client.move(np.array([x_initial, y_initial, clearance_height+height, 0, 1.57, np.pi/4]))
    time.sleep(2)
    client.move(np.array([x_initial, y_initial, height, 0, 1.57, np.pi/4]))
    time.sleep(2)
    client.move_gripper(0.0)
    time.sleep(2)
    client.move(np.array([x_initial, y_initial, clearance_height+height, 0, 1.57, np.pi/4]))
    time.sleep(2)
    client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.57, np.pi/4]))
    time.sleep(2)
    client.move(np.array([x_final, y_final, height, 0, 1.57, np.pi/4]))
    time.sleep(2)
    client.move_gripper(1.0)
    time.sleep(2)
    client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.57, np.pi/4]))
    time.sleep(2)


# def step_8(initial_pos, client):
#     """
#     Starts at left-hand side of the board from the robot's stand. Steps through
#     all 8 moves from left to right. If the orbot were playing black, it would 
#     step through ranks a-h
#     """
#     print(f"Stepping 8 tiles from ({initial_pos[0]}, {initial_pos[1]})")
#     for step in range(8):
#         client.move(np.array([initial_pos[0], initial_pos - (step * 0.05), 0.1, 0, 1.57, 0]))
#         time.sleep(3)

A1 = (0.45, 0.15)  # xy of A1 tile
initial_tile = A1
poses = [initial_tile] # each index represents a tile from a1 to h8
for file in range(8):
    file_step = file * 0.0434
    for rank in range(8):
        rank_step = rank * 0.0425
        poses.append((initial_tile[0] - file_step, initial_tile[1] - rank_step))
        
def main():
    parser = argparse.ArgumentParser(description='Pick and Place for WidowX Robot')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
    print("Starting robot.")

    is_open = 1
    try:
        playing = True
        is_move = False
        while playing:
            # Go home
            client.move(np.array([0.1, 0, 0.1, 0, 1.57, 0])) # Move home
            time.sleep(2)
            print_yellow("Enter moves as [x y] where x is the index of the square the piece starts at, and y is the square the piece moves to.")
            # player_move = input("Your move: ")
            # is_move = True
            # if is_move
            bot_move = input("Bot's move: ")
            if len(bot_move.split(" ")) != 2:
                print_yellow("Please enter two arguments.")
                continue

            from_square = int(bot_move.split(" ")[0])
            to_square = int(bot_move.split(" ")[1])

            client.move(np.array([0.3, 0, 0.15, 0, 1.57, 0])) # Move home
            time.sleep(2)
            height = 0.011
            clearance_height = 0.07
            pick_and_place(poses[from_square], poses[to_square], height, clearance_height, client)
            
            print_yellow("Move played.")




    except KeyboardInterrupt:
        time.sleep(1)
        client.reset()
        time.sleep(1)
        client.stop()
    

if __name__ == "__main__":
    main()
