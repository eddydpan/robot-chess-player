'''
Uses april tags to find location of board. 
When a move is entered, determines  which squares the piece was moved between.
'''

import cv2
import apriltag
import config
import numpy as np
import matplotlib.pyplot as plt
from shapely.prepared import prep
from shapely.geometry import Polygon, Point
from skimage.metrics import structural_similarity

detector = apriltag.Detector()

capture = cv2.VideoCapture(2)

running = True

last_state = None

while running:
    _, init_frame = capture.read()
    
    # rotate frame so board is not angled
    (h, w) = init_frame.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    M3 = cv2.getRotationMatrix2D((cX, cY), 110, 1.0)

    translation_matrix = np.float32([[1, 0, -250], [0, 1, -50]])

    frame = cv2.warpAffine(init_frame, M3, (w, h))

    frame = cv2.warpAffine(frame, translation_matrix, (w, h))

    # find april tags in frame
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    april_tags = detector.detect(grey_frame)

    if last_state is None: last_state = grey_frame

    tag_dict = {}
    for tag in april_tags:
        tag_id = tag.tag_id


        tag_dict[config.Corner(tag.tag_id).name] = tag.corners
        corners = tag.corners

        # show corners and IDs for debugging
        # cv2.polylines(frame, [corners.astype(int)], True, (0, 255, 0), 2)
        # cv2.putText(frame, str(tag_id), (int(corners[0][0]), int(corners[0][1])), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1)
    
    # if all four expected april tags are visible, we can draw the board
    if len(tag_dict) == 4:
        corners = []
        for corner, idx in config.BoardCorners.items():
            cv2.circle(frame, tag_dict[corner][idx].astype(int), 5, (0, 255, 0), 2)
            corners.append(tag_dict[corner][idx])

        # outline square from board corners
        square = Polygon(corners)

        def create_grid(geom, nx, ny):
            min_x, min_y, max_x, max_y = geom.bounds

            grid_x = np.linspace(min_x, max_x, nx)
            grid_y = np.linspace(min_y, max_y, ny)

            grid = []
            for ix in range(len(grid_x) - 1):
                for iy in range(len(grid_y) - 1):
                    cell = Polygon([[grid_x[ix], grid_y[iy]],
                                       [grid_x[ix], grid_y[iy + 1]],
                                       [grid_x[ix + 1], grid_y[iy + 1]],
                                       [grid_x[ix + 1], grid_y[iy]]])
                    grid.append(cell)
            return grid
    
        def partition(geom, nx, ny):
            prepared_geom = prep(geom)
            grid = list(filter(prepared_geom.intersects, \
                               create_grid(geom, nx, ny)))
            return grid
    
        grid = partition(square, 9, 9)

        for cell in grid:
            ext_pts = cell.exterior.coords
            pts = np.array(ext_pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)



    ## FINDING MOVED PIECE

    # update saved board state
    if cv2.waitKey(1) == ord("u"):
        new_state = grey_frame

        score, diff = structural_similarity(last_state, new_state, full = True)

        cell_diffs = {}

        if grid:
            # sum the difference in each cell
            for cell in grid:
                ext_pts = cell.exterior.coords
                pts = np.array(ext_pts, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(diff, [pts], True, (0, 0, 255), 1)
                
                min_x, min_y, max_x, max_y = cell.bounds
                cell_diff = 0

                for x in range(int(min_x), int(max_x)):
                    for y in range(int(min_y), int(max_y)):
                        cell_diff += diff[y][x]
                        
                
                cell_diffs[cell] = cell_diff
                

        
        
        sorted_cells = sorted(cell_diffs, key = cell_diffs.get)
        print(sorted(list(cell_diffs.values())))

        for i in range(0, 2):
            ext_pts = sorted_cells[i].exterior.coords
            pts = np.array(ext_pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(diff, [pts], True, (0, 0, 255), 5)

        # print(diff)

        cv2.imshow('Difference', diff)

        


    # show annotated image
    cv2.imshow("April Tag Tracking", frame)

    # press q to quit
    if cv2.waitKey(1) == ord("q"):
        running = False

capture.release()
cv2.destroyAllWindows()
