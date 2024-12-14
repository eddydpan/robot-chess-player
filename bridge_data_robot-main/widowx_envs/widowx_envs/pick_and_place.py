#!/usr/bin/env python3

import argparse
import numpy as np
import math
import time
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus

def distance_from_zero_zero(point):
    """
    Calculate the distance between [0, 0] and another point [x, y2.

    Args:
        point (list or tuple): Coordinates of the point [x, y].

    Returns:
        float: Distance between [0, 0] and the input point.
    """
    x, y = point
    distance = math.sqrt(x**2+y**2)
    return distance

def distance_between_points(point1, point2):
    """
    Calculate the distance between two points in a 2D plane.

    Args:
        point1 (list or tuple): Coordinates of the first point [x1, y1].
        point2 (list or tuple): Coordinates of the second point [x2, y2].

    Returns:
        float: Distance between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def find_pickup_droop(pickup_point):
    a = distance_from_zero_zero(pickup_point)
    droop = -2.35E-03 + 0.0522*a + -0.216*a**2
    return droop

def find_placing_droop(pickup_point, place_point):
    pickup_disp = distance_from_zero_zero(pickup_point)
    place_disp = distance_from_zero_zero(place_point)
    xy_increase = place_disp - pickup_disp
    return xy_increase * 0.0742


def pick_and_place(xy_initial, xy_final, height, clearance_height, client, gripper_width=1,blocking=True):
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

    pickup_droop = find_pickup_droop(xy_initial)
    placing_droop = find_placing_droop(xy_initial, xy_final)

    height -= pickup_droop

    client.move_gripper(gripper_width)
    time.sleep(4)
    move = client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0]),blocking=blocking) # Move home

    if move == 2: # in case it can't find a path directly to its final point
        client.step_action(np.array([-0.05, 0, 0, 0, 0,0,np.pi / 4]),blocking=blocking)
        time.sleep(1.5)
        client.move(np.array([0.15, 0, 0.15, 0, 1.5, np.pi / 4]),blocking=blocking) # Move home

    time.sleep(1.5)
    client.move(np.array([x_initial, y_initial, clearance_height+height, 0, 1.5, np.pi / 4]),blocking=blocking)
    time.sleep(1.5)
    client.move(np.array([x_initial, y_initial, height, 0, 1.5, np.pi / 4]),blocking=blocking)
    time.sleep(1.5)
    client.move_gripper(0.0)
    time.sleep(1.5)
    client.move(np.array([x_initial, y_initial, clearance_height+height, 0, 1.5, np.pi / 4]),blocking=blocking)
    time.sleep(1.5)

    move = client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.5, np.pi / 4]),blocking=blocking)
    print(move)
    if move == 2: # in case it can't find a path directly to its final point
        client.step_action(np.array([-0.05, 0, 0, 0, 0,0,np.pi / 4]),blocking=blocking)
        time.sleep(1.5)
        client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.5, np.pi / 4]),blocking=blocking)
        
    time.sleep(1.5)
    client.move(np.array([x_final, y_final, height+placing_droop+0.002, 0, 1.5, np.pi / 4]),blocking=blocking)
    time.sleep(1.5)
    # client.step_action(np.array([0, 0, 0, 0, 0, 0,gripper_width]),blocking=blocking)
    client.move_gripper(gripper_width) # moves to narrow if narrow, otherwise opens fully
    time.sleep(1.5)
    client.move(np.array([x_final, y_final, clearance_height+height, 0, 1.5, np.pi / 4]),blocking=blocking)
    # time.sleep(4)
    

def main():
    parser = argparse.ArgumentParser(description='Pick and Place for WidowX Robot')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)

    is_open = 1

    pick_and_place([0.45, -0.14], [0.3, 0], 0.02, 0.08, client, gripper_width=0.7)

    pick_and_place([0.3, 0], [0.15, -0.14], 0.02, 0.08, client, gripper_width=0.7)

    pick_and_place([0.15, -0.14], [0.15, 0], 0.02, 0.08, client, gripper_width=0.7)

    # pick_and_place([0.15, -0.14], [0.3, 0.28], 0.023, 0.08, client, gripper_width=0.7)
    # time.sleep(4)
    # time.sleep(5)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.375, 0, 0.1, 0, 1.5, 0]))
    # time.sleep(5)
    # client.move(np.array([0.375, 0, 0.04, 0, 1.5, 0]))
    # time.sleep(20)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.375,0, 0.1, 0, 1.5, 0]))
    # time.sleep(5)
    # client.move(np.array([0.375, 0, 0.04, 0, 1.5, 0]))
    # time.sleep(20)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.425,0, 0.1, 0, 1.5, 0]))
    # time.sleep(5)
    # client.move(np.array([0.425, 0, 0.04, 0, 1.5, 0]))
    # time.sleep(20)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.3,0, 0.1, 0, 1.5, 0]))
    # time.sleep(5)
    # client.move(np.array([0.3, 0, 0.04, 0, 1.5, 0]))
    # time.sleep(20)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.375,0, 0.1, 0, 1.5, 0]))
    # time.sleep(20)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.425,0, 0.1, 0, 1.5, 0]))
    # time.sleep(20)
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0])) # Move home
    # time.sleep(5)
    # client.move(np.array([0.475,0, 0.1, 0, 1.5, 0]))
    # time.sleep(10)


    client.stop()  # Properly stop the client
    print("Pick and place complete.")

if __name__ == "__main__":
    main()
