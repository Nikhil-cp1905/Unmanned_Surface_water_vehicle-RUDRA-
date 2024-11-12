import numpy as np
from filterpy.kalman import ExtendedKalmanFilter
import random
import matplotlib.pyplot as plt

gps_noise_std = 1.0  
imu_noise_std = 0.1  
dt = 0.1  

true_x = 0
true_y = 0
true_vx = 1.0  # Constant velocity in x
true_vy = 0.5  # Constant velocity in y
num_steps = 100  # Total simulation steps

# EKF initialization
ekf = ExtendedKalmanFilter(dim_x=4, dim_z=2)
ekf.x = np.array([0, true_vx, 0, true_vy])  # Initial state
ekf.P *= 1000  # Uncertainty
ekf.R = np.diag([gps_noise_std**2, gps_noise_std**2])  # GPS noise covariance
ekf.Q = np.eye(4) * 0.1  # Process noise covariance

# State transition and measurement functions
def transition_function(state):
    x, vx, y, vy = state
    return np.array([x + vx * dt, vx, y + vy * dt, vy])

def measurement_function(state):
    x, _, y, _ = state
    return np.array([x, y])

# Lists for storing results for plotting
true_positions = []
ekf_positions = []

for _ in range(num_steps):
    # Simulate true position
    true_x += true_vx * dt
    true_y += true_vy * dt
    true_positions.append((true_x, true_y))
    
    # Simulate GPS reading with noise
    gps_x = true_x + random.gauss(0, gps_noise_std)
    gps_y = true_y + random.gauss(0, gps_noise_std)

    # Simulate IMU reading (here we assume constant acceleration for simplicity)
    ax = random.gauss(0, imu_noise_std)  # Simulated acceleration in x
    ay = random.gauss(0, imu_noise_std)  # Simulated acceleration in y

    # Dead reckoning (for simplicity we will just update the velocity)
    ekf.x[0] += ekf.x[1] * dt + 0.5 * ax * dt**2  # Update position x
    ekf.x[2] += ekf.x[3] * dt + 0.5 * ay * dt**2  # Update position y

    # EKF predict
    ekf.F = np.array([[1, dt, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, dt],
                      [0, 0, 0, 1]])
    
    ekf.predict()

    # Update with GPS measurement
    z = np.array([gps_x, gps_y])
    ekf.update(z, HJacobian=lambda x: np.array([[1, 0, 0, 0], [0, 0, 1, 0]]), Hx=measurement_function)

    # Store estimated position for plotting
    ekf_positions.append((ekf.x[0], ekf.x[2]))

# Convert positions for plotting
true_positions = np.array(true_positions)
ekf_positions = np.array(ekf_positions)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(true_positions[:, 0], true_positions[:, 1], label='True Position', color='g', linewidth=2)
plt.plot(ekf_positions[:, 0], ekf_positions[:, 1], label='EKF Estimated Position', color='r', linestyle='--')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('EKF Position Estimation vs True Position')
plt.legend()
plt.grid()
plt.axis('equal')  # Set equal scaling on x and y axes
plt.tight_layout()  # Adjust layout to fit elements
plt.show()  # Ensure the plot is displayed

