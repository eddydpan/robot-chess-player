"""
A Python module where the WidowX-200's end effector touches  all four corners of our chess board.
"""


#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import time
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus
    
def pick_up(client, dist, is_open):

    # Move down
    client.step_action(np.array([0,0,-0.1,0,0,0,is_open]))
    time.sleep(2)
    client.step_action(np.array([0,0,-0.1,0,0,0,is_open]))
    time.sleep(2)
    
    # Grab Piece
    is_open = 0
    client.move_gripper(0.0)
    time.sleep(2)

    # Move up
    client.step_action(np.array([0,0,0.1,0,0,0,is_open]))
    time.sleep(2)
    client.step_action(np.array([0,0,0.1,0,0,0,is_open]))
    time.sleep(2)

    # # Move +x +y
    # client.step_action(np.array([0,0.2,0,0,0,0,is_open]))
    # time.sleep(2)
    # client.step_action(np.array([0,0.2,0,0,0,0,is_open]))
    # time.sleep(2)

    # Bring it back down
    client.step_action(np.array([0,0,-0.1,0,0,0,is_open]))
    time.sleep(2)
    client.step_action(np.array([0,0,-0.1,0,0,0,is_open]))
    time.sleep(2)

    # Close the gripper
    client.move_gripper(1.0)
    is_open = 1
    time.sleep(2)

    # Go back up enough above the pieces
    client.step_action(np.array([0,0,0.1,0,0,0,is_open]))
    time.sleep(1)
    client.step_action(np.array([0,0,0.1,0,0,0,is_open]))
    time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description='Pick and Place for WidowX Robot')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)

    is_open = 1

    print("Starting robot.")

    
    # Move to starting position
    time.sleep(2)
    client.move(np.array([0.3, 0.1, 0.1, 0, 1.57, 0]))
    time.sleep(2)

    # Move to Quadrant 1's corner
    client.move(np.array([0.45, 0.15, 0.08, 0, 1.57, np.pi/4]))
    time.sleep(5)

    # Return home
    client.move(np.array([0.3, 0.1, 0.1, 0, 1.57, 0]))
    time.sleep(2)

    # # Move to Quadrant 2's corner
    # client.move(np.array([0.35, 0, 0.1, 0, 1.57, 0]))
    # time.sleep(2)
    # client.move(np.array([0.45, -0.15, 0.1, 0, 0, np.pi/4]))
    # time.sleep(2)

    # # Return home
    # client.move(np.array([0.3, 0, 0.1, 0, 1.57, 0]))
    # time.sleep(2)

    # # Move to Quadrant 3's corner
    # client.move(np.array([0.175, -0.15, 0.1, 0, 1.45, np.pi/4]))
    # time.sleep(2)
    
    # # Return home   
    # client.move(np.array([0.3, 0, 0.1, 0, 1.57, 0]))
    # time.sleep(2)

    # # Move to Quadrant 4's corner
    # client.move(np.array([0.17, 0.15, 0.15, 0, 1.57, -np.pi/4]))
    # time.sleep(2)

    # # Pick up Q4 corner piece
    # # pick_up(client, 0.1, is_open)
    # # Move down
    # client.move(np.array([0.17, 0.15, 0.1, 0, 1.57, -np.pi/4]))
    # time.sleep(2)

    # client.move(np.array([0.17, 0.15, 0.05, 0, 1.57, -np.pi/4]))
    # time.sleep(2)

    # # Return home
    # client.move(np.array([0.15, 0, 0.1, 0, 1.57, 0]))
    # time.sleep(2)
    
    
    client.stop()  # Properly stop the client

if __name__ == "__main__":
    main()
