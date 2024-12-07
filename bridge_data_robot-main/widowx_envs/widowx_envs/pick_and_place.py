#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import time
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus

def pick_and_place(xy_initial, xy_final, height, clearance_height, client, gripper_width=1):
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
    y_final = xy_final[1]

    client.move_gripper(gripper_width)

    client.move(np.array([0.3, 0, 0.15, 0, 1.57, 0])) # Move home
    time.sleep(4)
    client.move(np.array([x_initial, y_initial, clearance_height+height, 0, 1.57, 0]))
    time.sleep(4)
    client.move(np.array([x_initial, y_initial, height, 0, 1.57, 0]))
    time.sleep(4)
    client.move_gripper(0.0)
    time.sleep(4)
    client.move(np.array([x_initial, y_initial, clearance_height+height, 0, 1.57, 0]))
    time.sleep(4)
    client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.57, 0]))
    time.sleep(4)
    client.move(np.array([x_final, y_final, height, 0, 1.57, 0]))
    time.sleep(4)
    client.move_gripper(gripper_width) # moves to narrow if narrow, otherwise opens fully
    time.sleep(4)
    client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.57, 0]))
    time.sleep(4)



    

def main():
    parser = argparse.ArgumentParser(description='Pick and Place for WidowX Robot')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)

    is_open = 1

    pick_and_place([0.17, -0.1], [0.17, -0.02], 0.04, 0.08, client, gripper_width=0.7)

    # client.move(np.array([0.3, 0, 0.15, 0, 1.57, 0]))
    # time.sleep(5)
    # # client.move_gripper(1.0)
    # # time.sleep(2)
    # # client.move_gripper(0.5)
    # # time.sleep(3)
    # # client.move_gripper(0.2)
    # # time.sleep(2)
    # # client.move_gripper(0.0)
    # client.step_action(np.array([-0.06,0,0,0,0,0,is_open]))
    # time.sleep(5)
    # client.step_action(np.array([0,0,-0.05,0,0,0,is_open]))
    # time.sleep(5)
    # is_open = 0.1
    # client.move_gripper(0.1)
    # time.sleep(5)
    # client.step_action(np.array([0,0,0.15,0,0,0,is_open]))
    # time.sleep(5)
    # client.step_action(np.array([0.1,0.1,0,0,0,0,is_open]))
    # time.sleep(5)
    # client.step_action(np.array([0,0,-0.15,0,0,0,is_open]))
    # time.sleep(5)
    # client.move_gripper(1.0)
    # is_open = 1
    # time.sleep(5)
    # client.step_action(np.array([0,0,0.15,0,0,0,is_open]))
   



    client.stop()  # Properly stop the client
    print("Pick and place complete.")

if __name__ == "__main__":
    main()
