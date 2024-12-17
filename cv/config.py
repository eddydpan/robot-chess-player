from enum import Enum
# orientation of L/R is facing the board from
# perspective of either robot or player

class Corner(Enum):
    ROBOT_L = 96
    PLAYER_R = 98
    PLAYER_L = 99
    ROBOT_R = 97


# which corners of the april tags are the corners of the board
BoardCorners = {
    "ROBOT_L": 0,
    "PLAYER_R": 2,
    "PLAYER_L": 1,
    "ROBOT_R": 3
}
