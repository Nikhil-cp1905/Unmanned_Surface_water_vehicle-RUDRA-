import matplotlib.pyplot as plt
import numpy as np
from d_star_lite import DStarLite  # Import the D* Lite algorithm
from grid_map import GridMap  # Your existing grid map implementation

def main():
    obstacles = [
        np.array([[0.7, -0.9], [1.3, -0.9], [1.3, -0.8], [0.7, -0.8]]) + np.array([-1.0, 0.5]),
        np.array([[0.7, -0.9], [1.3, -0.9], [1.3, -0.8], [0.7, -0.8]]) + np.array([-1.0, 1.0]),
        np.array([[0.7, -0.9], [0.8, -0.9], [0.8, -0.3], [0.7, -0.3]]) + np.array([-1.0, 0.5]),        
    ]

    flight_area_vertices = 2 * np.array([[-0.6, 0.8], [-0.9, -0.9], [0.8, -0.8], [0.5, 0.9]])
    gridmap = GridMap(flight_area_vertices)
    gridmap.add_obstacles_to_grid_map(obstacles)

    start = np.array([-1.0, -1.0])
    goal = np.array([0.5, 0.9])
    
    # Convert start and goal to grid coordinates
    start_grid = gridmap.meters2grid(start)
    goal_grid = gridmap.meters2grid(goal)

    # Initialize the D* Lite planner
    dstar = DStarLite(gridmap.gmap, tuple(start_grid), tuple(goal_grid))
    path = dstar.plan()  # Get the planned path

    # Plotting and following the path
    plt.figure(figsize=(10, 10))
    gridmap.draw_map(obstacles)
    plt.plot(goal[0], goal[1], 'ro', markersize=20, label='Goal position')
    
    # Follow the path
    for pose in path:
        # Convert grid coordinates back to meters for plotting
        pose_m = gridmap.grid2meters(np.array(pose))
        plt.plot(pose_m[0], pose_m[1], 'bo')  # Plot the path
        plt.pause(0.1)

    plt.show()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
