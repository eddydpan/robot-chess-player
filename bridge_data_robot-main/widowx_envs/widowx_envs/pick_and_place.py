#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import time
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus

def show_video(client, full_image=True):
    """
    This shows the video from the camera for a given duration.
    Full image is the image before resized to default 256x256.
    """
    res = client.get_observation()
    if res is None:
        print("No observation available... waiting")
        return

    if full_image:
        img = res["full_image"]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        img = res["image"]
        img = (img.reshape(3, 256, 256).transpose(1, 2, 0) * 255).astype(np.uint8)
    cv2.imshow("Robot Camera", img)
    cv2.waitKey(20)  # 20 ms

print_yellow = lambda x: print("\033[93m {}\033[00m" .format(x))


def print_help():
    print_yellow("  Teleop Controls:")
    print_yellow("    w, s : move forward/backward")
    print_yellow("    a, d : move left/right")
    print_yellow("    z, c : move up/down")
    print_yellow("    i, k:  rotate yaw")
    print_yellow("    j, l:  rotate pitch")
    print_yellow("    n  m:  rotate roll")
    print_yellow("    space: toggle gripper")
    print_yellow("    r: reset robot")
    print_yellow("    q: quit")

def pick_and_place(xy_initial, xy_final, height, clearance_height, client, narrow=False):
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

    if narrow:
        client.move_gripper(0.5)
        time.sleep(2)

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
    client.move_gripper(1.0 - 0.5 * narrow) # moves to narrow if narrow, otherwise opens fully
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

    print_help()
    is_open = 1

    client.move(np.array([0.3, 0, 0.15, 0, 1.57, 0]))
    time.sleep(5)
    # client.move_gripper(1.0)
    # time.sleep(2)
    # client.move_gripper(0.5)
    # time.sleep(3)
    # client.move_gripper(0.2)
    # time.sleep(2)
    # client.move_gripper(0.0)
    client.step_action(np.array([-0.06,0,0,0,0,0,is_open]))
    time.sleep(5)
    client.step_action(np.array([0,0,-0.05,0,0,0,is_open]))
    time.sleep(5)
    is_open = 0.1
    client.move_gripper(0.1)
    time.sleep(5)
    client.step_action(np.array([0,0,0.15,0,0,0,is_open]))
    time.sleep(5)
    client.step_action(np.array([0.1,0.1,0,0,0,0,is_open]))
    time.sleep(5)
    client.step_action(np.array([0,0,-0.15,0,0,0,is_open]))
    time.sleep(5)
    client.move_gripper(1.0)
    is_open = 1
    time.sleep(5)
    client.step_action(np.array([0,0,0.15,0,0,0,is_open]))
   



    client.stop()  # Properly stop the client
    print("Pick and place complete.")

if __name__ == "__main__":
    main()
