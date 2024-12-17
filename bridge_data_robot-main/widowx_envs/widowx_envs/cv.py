import cv2
import apriltag
import numpy as np
import shapely.geometry as geom
from shapely.prepared import prep

class BoardView():
    # CONFIG
    '''class Corner():
        def __init__(self, name, tag_id, corner_idx):
            self.name = name
            self.tag_id = tag_id
            self.corner_idx = corner_idx
    
    corners = [
        Corner("ROBOT_L", 96, 0),
        Corner("PLAYER_R", 98, 2),
        Corner("PLAYER_L", 99, 1),
        Corner("ROBOT_R", 97, 3)
    ]'''

    def __init__(self):
        self.cap = cv2.VideoCapture(2)

        _, frame = self.cap.read()

        self.H, self.W = frame.shape[:2]
        self.CENTER = (self.W // 2, self.H // 2)

        # rotate and translate frame for best view
        self.__rotate_frame(110)
        self.__translate_frame(-250, -50)

        # last saved board state
        self.last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def __find_tags(self):
        detector = apriltag.Detector()
        april_tags = detector.detect(self.frame)

        tag_dict = {}

        for tag in april_tags:
            tag_dict['''fix this!'''] = tag.corners
        

        return tag_dict
    
    def __get_corners(self, tag_dict):
        board_corners = []

        for corner, idx in config.BoardCorners.items():
            board_corners.append(tag_dict[corner][idx])
        
        return board_corners

    def __create_grid(self, corners):
        nx = 9
        ny = 9

        square = geom.Polygon(corners)
        min_x, min_y, max_x, max_y = square.bounds

        grid_x = np.linspace(min_x, max_x, nx)
        grid_y = np.linspace(min_y, max_y, ny)

        grid = []
        for ix in range(len(grid_x) - 1):
            for iy in range(len(grid_y) - 1):
                cell = geom.Polygon([
                    [grid_x[ix], grid_y[iy]],
                    [grid_x[ix], grid_y[iy + 1]],
                    [grid_x[ix + 1], grid_y[iy + 1]],
                    [grid_x[ix + 1], grid_y[iy]]
                ])
                grid.append(cell)
        
        # i feel like odds are i dont need this line
        # grid = list(filter(prep(square).intersects, grid))


        self.board_cells = {}

        letters = "hgfedcba"
        idx = 0
        num = 0

        for cell in grid:
            # i think this is gonna name them right but we'll see
            cell_label = letters[idx] + str(num + 1)
            self.board_cells[cell_label] = cell

            if num == 7:
                num = 0
                idx += 1
                
    
    def locate_board(self, draw = False):
        tag_dict = self.__find_tags()
        
        if(len(tag_dict) != '''expected num tags'''):
            print("thats bad")
            return
        
        self.__get_corners(tag_dict)
        



    def __rotate_frame(self, theta):
        R = cv2.getRotationMatrix2D(self.CENTER, theta, 1.0)
        self.frame = cv2.warpAffine(self.frame, R, (self.W, self.H))
    
    def __translate_frame(self, x, y):
        T = np.float32([[1, 0, x], [0, 1, y]])
        self.frame = cv2.warpAffine(self.frame, T, (self.W, self.H))


