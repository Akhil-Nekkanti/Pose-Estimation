import inputParser as ip
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json

def process_poses(poses):
    pose_joint_tuples = {}
    for i in range(len(poses)):
        ptuples = [tuple(poses[i]['camera_position'])]
        for j in range(0, len(poses[i]['joint_coordinates']), 3):
            x, y, z = poses[i]['joint_coordinates'][j:j+3]
            ptuples.append((x, y, z))
        pose_joint_tuples[i] = ptuples
    return pose_joint_tuples

def calculate_viewpoint(point):
    x, y, z = point
    elev = np.degrees(np.arctan2(z, np.sqrt(x**2 + y**2)))  # Elevation angle
    azim = np.degrees(np.arctan2(y, x))  # Azimuth angle
    return elev, azim

def plot_poses(pposes):
    '''
    pposes is a dictionary where the key is the identifier of the pose
    and the value is a list of tuples.
    The first tuple is the camera position and the rest are the joint coordinates.
    This code orients the graph and plots the points as a scatter plot.
    Needs to be modified to show the joints as connected by lines (skeleton).
    '''
    for identifier, points in pposes.items():
        # Create a new 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Calculate the viewpoint using the first point
        first_point = points[0]
        elev, azim = calculate_viewpoint(first_point)
        ax.view_init(elev=elev, azim=azim)

        # Unpack the list of tuples into three separate lists: x, y, and z coordinates
        x_coords, y_coords, z_coords = zip(*points[1:])  # Skip the first point

        # Plot the points
        ax.scatter(x_coords, y_coords, z_coords)

        # Label the axes and add a title
        ax.set_title(identifier)
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        
        bconnections = [(0, 1), (0, 4), (0, 7), (7, 8), (7, 11)]
        rconnections = [(8, 9), (9, 10), (4, 5), (5, 6)]
        blconnections = [(11, 12), (12, 13), (1, 2), (2, 3)]
        
        for start, end in bconnections:
            x_line = [x_coords[start], x_coords[end]]
            y_line = [y_coords[start], y_coords[end]]
            z_line = [z_coords[start], z_coords[end]]

            ax.plot(x_line, y_line, z_line, color='black')
        for start, end in rconnections:
            x_line = [x_coords[start], x_coords[end]]
            y_line = [y_coords[start], y_coords[end]]
            z_line = [z_coords[start], z_coords[end]]

            ax.plot(x_line, y_line, z_line, color='red')
        
        for start, end in blconnections:
            x_line = [x_coords[start], x_coords[end]]
            y_line = [y_coords[start], y_coords[end]]
            z_line = [z_coords[start], z_coords[end]]

            ax.plot(x_line, y_line, z_line, color='blue')
        # Balance Ranges
        x_range = np.max(x_coords) - np.min(x_coords)
        y_range = np.max(y_coords) - np.min(y_coords)
        z_range = np.max(z_coords) - np.min(z_coords)

        # Normalize the aspect ratio by scaling x, y, and z equally
        max_range = max(x_range, y_range, z_range)  # Find the largest range
        ax.set_box_aspect([x_range / max_range, y_range / max_range, z_range / max_range])
                
        # Show the plot
        plt.show()

def table_of_2d_points(pposes):
    '''
    Needs to create a table of 2D points for each pose
    One table for all the poses.
    (use the focal points to convert 3d to 2d).
    '''
    focal_length = ip.parse_focal_length('focal.txt')  # Parse the focal length from the file

    # Initialize the dictionary to store 2D projections
    projections = {}

    for pose_id, points in pposes.items():
        projections[pose_id] = []
        for i, (x, y, z) in enumerate(points[1:]):  # Skip the first point (camera position)
            # Project the 3D point onto the 2D plane using the pinhole camera model
            u = focal_length * (x / z)
            v = focal_length * (y / z)

            # Store the 2D projection in the dictionary
            projections[pose_id].append((u, v))

    return projections

if '__main__' == __name__:
    focal_length = ip.parse_focal_length('focal.txt')
    joint_names = ip.parse_joint_names('joint-names.txt')
    poses = ip.parse_poses('poses.txt')
    pposes = process_poses(poses)
    #plot_poses(pposes)
    
    projections = table_of_2d_points(pposes)
    print(projections)
    #with open('pposes.txt', 'w') as f:
        #json.dump(pposes, f, indent = 4)
    #with open('projections.txt', 'w') as f:
        #json.dump(projections, f, indent = 4)