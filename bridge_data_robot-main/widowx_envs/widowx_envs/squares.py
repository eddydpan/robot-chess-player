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


def step_8(initial_pos, client):
    """
    Starts at left-hand side of the board from the robot's stand. Steps through
    all 8 moves from left to right. If the orbot were playing black, it would 
    step through ranks a-h
    """
    print(f"Stepping 8 tiles from ({initial_pos[0]}, {initial_pos[1]})")
    for step in range(8):
        client.move(np.array([initial_pos[0], initial_pos - (step * 0.05), 0.1, 0, 1.57, 0]))
        time.sleep(3)
    

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
    client.move(np.array([0.3, 0, 0.1, 0, 1.57, 0]))
    time.sleep(4)

    # Move to Q4 Corner (a1 if robo playing black)
    q1 = np.array([0.45, 0.15, 0.1, 0, 1.57, 0])
    client.move(q1)
    time.sleep(2)

    board = []
    initial_pos = q1
    for file in range(8):
        rank_step = 0.0
        file_step = file * 0.0434
        client.move(np.array([initial_pos[0] - file_step, initial_pos[1] - rank_step, 0.09, 0, 1.57, np.pi/4]))
        time.sleep(3)
        print(f"Stepping 8 tiles from ({initial_pos[0] - file_step}, {initial_pos[1] - rank_step})")
        for rank in range(8):
            rank_step = rank * 0.0425
            client.move(np.array([initial_pos[0] - file_step, initial_pos[1] - rank_step, 0.09, 0, 1.57, np.pi/4]))
            time.sleep(1)
            # client.move(np.array([initial_pos[0] + file_step, initial_pos[1] - rank_step, 0.04, 0, 1.57, np.pi/4]))
            # time.sleep(1)
            # client.move(np.array([initial_pos[0] + file_step, initial_pos[1] - rank_step, 0.08, 0, 1.57, np.pi/4]))
            # time.sleep(1)

            board.append((initial_pos[0] - file_step, initial_pos[1] - rank_step))
    try:
        np.savetxt('board_poses3.csv', board, delimiter=', ', fmt= "% s")
    except:
        breakpoint()
if __name__ == "__main__":
    main()
