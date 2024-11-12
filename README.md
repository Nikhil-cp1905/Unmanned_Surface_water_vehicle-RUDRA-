# Unmanned Surface Water Vehicle - RUDRA 🌊

**An autonomous surface water vehicle built to navigate, detect obstacles, and follow defined paths.**  
[![RUDRA Project](images/hero_image.jpg)](images/hero_image.jpg)

### Overview
USV (unmanned Surface water vehicle) is designed to autonomously navigate surface water environments. With GPS, IMU, and real-time obstacle detection, RUDRA adjusts its path dynamically using D* Lite path-planning to avoid collisions. This makes it suitable for water-based tasks like monitoring, sample collection, and environmental studies.

## Features
### Autonomous Navigation
RUDRA leverages GPS and IMU for geolocation and direction control. The Kalman Filter integrates sensor data for accuracy, while dead reckoning estimates position during GPS signal loss.

### D* Lite Path Planning Algorithm
D* Lite path-planning enables RUDRA to dynamically navigate around obstacles detected mid-journey, recalculating the most efficient path to the target.

### Obstacle Detection
Using Time-of-Flight (TOF) sensors and OpenCV for object recognition, RUDRA identifies obstacles, recalculating its path in real-time to avoid them.
_____
____

# WORK DONE
____________
## Autonomouss
### DeadReckoning 
This Python code implements an Extended Kalman Filter (EKF) for estimating the position of a moving object with noisy sensor data, utilizing libraries like numpy, filterpy, and matplotlib. The simulation assumes constant velocity in the x and y directions, updating the position at each time step (dt). It calculates a "true" position as a reference, with simulated GPS readings affected by Gaussian noise and random IMU readings modeling acceleration noise. The EKF predicts the object's position, using noisy GPS data to correct its state estimate. The trajectory of both the true position and EKF estimate is plotted, demonstrating the filter's effectiveness in tracking the object despite measurement uncertainty.
![Screenshot from 2024-11-02 01-24-15](https://github.com/user-attachments/assets/3cd14d87-7053-4e3a-a1f0-228b62ff5340)


### Width of objects
This Python script captures video from a camera to measure object dimensions using computer vision. It initializes the camera, continuously capturing frames while preprocessing each frame to grayscale, applying Gaussian blur, and detecting edges with the Canny algorithm. The script identifies contours of detected objects, filtering them by size and assuming the largest contour as a reference for calibration. It calculates a pixel-to-centimeter ratio based on this reference object’s known dimensions and measures the width and height of other detected objects. These measurements are displayed on the processed frames in real-time,continuing until the user presses 'q' to close the application.
![Screenshot from 2024-11-02 01-26-42](https://github.com/user-attachments/assets/6205355a-eed4-4d83-9bc4-b87a3b96f14a)

### Distance Between Objects
This Python script uses OpenCV for distance estimation to an object via a stereo vision approach, simulating a dual-camera setup with a single camera. It captures two consecutive frames with a brief delay, flipping the second frame to mimic a right-side camera perspective. After converting the frames to grayscale, it extracts keypoints and descriptors using the ORB feature detector and matches features between the frames with a brute-force matcher. The distance is calculated based on the average disparity of the matched features, using a known baseline and the camera's focal length, which the user inputs at runtime. The estimated distance is displayed on a combined image of the matched features, continuing until the user presses 'q' to exit. The script then releases camera resources and closes OpenCV windows for real-time distance estimation.
![Screenshot from 2024-11-02 01-27-58](https://github.com/user-attachments/assets/0f100025-49d8-4040-975d-72c07437a685)


_______________
## Sensors
### Dissolved Oxygen
A dissolved oxygen sensor is a vital instrument used to measure the concentration of oxygen in water. It plays a crucial role in monitoring aquatic ecosystems, ensuring the health of marine life, and managing water quality in various environments, including rivers, lakes, and wastewater treatment facilities. These sensors typically operate based on electrochemical or optical principles, providing real-time data that is essential for assessing the effects of pollution and climate change on aquatic habitats. By enabling precise tracking of oxygen levels, dissolved oxygen sensors facilitate informed decision-making for environmental protection and resource management, ultimately supporting the sustainability of our water bodies.
![Screenshot from 2024-11-02 01-29-45](https://github.com/user-attachments/assets/f33dfbed-2295-4e7f-834c-538ad78d4e02)  ![Screenshot from 2024-11-02 01-31-51](https://github.com/user-attachments/assets/5baef747-8f5c-48d4-905e-1611dccb0ed1)

### PHsensor
A pH sensor is an essential device used to measure the acidity or alkalinity of a solution. Operating on electrochemical principles, it provides real-time data crucial for various applications, including environmental monitoring, agriculture, and water treatment. By measuring the hydrogen ion concentration, pH sensors help maintain optimal conditions for aquatic life and crop growth. Their accurate readings support effective decision-making in laboratory experiments and industrial processes, ensuring quality and compliance with environmental standards
![Screenshot from 2024-11-02 01-33-49](https://github.com/user-attachments/assets/01988fff-eb51-4b48-b558-a94048ea9fe4)

### MQ4 - gas sensor
The MQ-4 gas sensor is a widely used device for detecting methane (CH4) and other combustible gases in the environment. Utilizing a sensitive ceramic element, it changes resistance based on gas concentration, enabling accurate measurements. This sensor is essential in applications such as gas leak detection, home safety systems, and air quality monitoring. Its affordability and ease of integration make it popular for both DIY projects and professional gas sensing solutions.
________________
## Path planning

### d_star_lite simulation
The code implements the D* Lite algorithm for dynamic pathfinding in a grid environment with obstacles. It defines a Node class for grid points, storing their coordinates and costs. The DStarLite class initializes with static obstacles and prepares a grid to track costs (g and rhs). Using a priority queue, the algorithm manages nodes based on calculated keys from heuristic and current costs. It updates the graph as new obstacles are detected, either through input or random generation, and assesses neighboring nodes for potential paths. The algorithm adapts to environmental changes, recalculating paths as necessary. It visualizes the process using matplotlib, plotting start and goal locations, paths, and obstacles. The detect_changes method checks for new obstacles each iteration, ensuring the search space remains valid. The computed path is displayed until the goal is reached, providing real-time updates on environmental modifications, making D* Lite effective for robotics and autonomous vehicles.
![Screenshot from 2024-11-02 01-25-36](https://github.com/user-attachments/assets/45c89696-5013-4d1b-83fd-128ba8fa0b65)

### IMU and GPS map Track
In path planning, Inertial Measurement Units (IMUs) and GPS work together to provide accurate navigation data. IMUs, consisting of accelerometers and gyroscopes, track the device's movement and orientation, offering real-time feedback on speed and direction. GPS complements this by providing absolute positioning information. By integrating data from both sensors, algorithms can effectively estimate the vehicle's trajectory, adjust paths dynamically, and enhance navigation accuracy, making them essential for robotics and autonomous vehicles.
![Screenshot from 2024-11-02 01-41-24](https://github.com/user-attachments/assets/7f20bc82-a6f3-4e8f-98d1-0b61dc09cf80)

____
____
# THIS IS MAP MADE USING RRT* BUT WE ARE FINALIZED WITH D*LITE (THIS IS JUST REPRESENTATION OF HOW IT LOOKS LIKE , NEED TO JUST CHANGE THE ALGORITHM TO D*LITE)
## Map Planned using RRT*
COST BASED MAP FORMED ,and Path Made also made using Localization , and proper PID
![Screenshot from 2024-11-02 01-43-36](https://github.com/user-attachments/assets/db5cf18c-24c9-4404-baf0-abc1deaae63e)


