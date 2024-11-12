#include <Servo.h>

// Define ESC connections
const int escPropeller1Pin = 9; // ESC for Propeller 1
const int escPropeller2Pin = 10; // ESC for Propeller 2
const int escThruster1Pin = 11; // ESC for Side Thruster 1
const int escThruster2Pin = 12; // ESC for Side Thruster 2

Servo escPropeller1;
Servo escPropeller2;
Servo escThruster1;
Servo escThruster2;

// Movement commands
enum Direction { FORWARD, BACKWARD, LEFT, RIGHT, STOP };
Direction currentDirection;

// Map definition (example with a 5x5 grid, 0 = free, 1 = obstacle)
int map[5][5] = {
    {0, 0, 0, 0, 0},
    {0, 1, 1, 1, 0},
    {0, 0, 0, 1, 0},
    {0, 1, 0, 0, 0},
    {0, 0, 0, 0, 0}
};

// Starting and goal positions (example)
int startX = 0, startY = 0; // Starting point
int goalX = 4, goalY = 4; // Goal point

void setup() {
    escPropeller1.attach(escPropeller1Pin);
    escPropeller2.attach(escPropeller2Pin);
    escThruster1.attach(escThruster1Pin);
    escThruster2.attach(escThruster2Pin);
    
    // Calibrate ESCs
    calibrateESC(escPropeller1);
    calibrateESC(escPropeller2);
    calibrateESC(escThruster1);
    calibrateESC(escThruster2);

    // Run the D* Lite algorithm to find a path
    int pathLength = findPath(startX, startY, goalX, goalY);
    
    // Execute the path
    for (int i = 0; i < pathLength; i++) {
        executeMovement(currentDirection);
    }
}

void loop() {
    // Do nothing in loop, all actions are in setup for this example
}

// Function to find a path using D* Lite (simplified version)
int findPath(int startX, int startY, int goalX, int goalY) {
    // This is a placeholder for your D* Lite algorithm implementation
    // This function should return the number of steps in the found path
    // For demonstration, we will assume a direct path
    return 5; // Change this to the actual path length
}

// Function to execute movement based on the current direction
void executeMovement(Direction dir) {
    switch (dir) {
        case FORWARD:
            setBoatSpeed(1500, 1500, 0, 0); // Move forward
            break;
        case BACKWARD:
            setBoatSpeed(1000, 1000, 0, 0); // Move backward
            break;
        case LEFT:
            setBoatSpeed(0, 0, 1500, 1500); // Move left
            break;
        case RIGHT:
            setBoatSpeed(0, 0, 1000, 1000); // Move right
            break;
        case STOP:
            setBoatSpeed(0, 0, 0, 0); // Stop
            break;
    }
    delay(3000); // Move for 3 seconds
}

// Function to set the speed of the boat motors
void setBoatSpeed(int propSpeed1, int propSpeed2, int thrustSpeed1, int thrustSpeed2) {
    escPropeller1.writeMicroseconds(propSpeed1);
    escPropeller2.writeMicroseconds(propSpeed2);
    escThruster1.writeMicroseconds(thrustSpeed1);
    escThruster2.writeMicroseconds(thrustSpeed2);
}

// Function to calibrate the ESC
void calibrateESC(Servo &esc) {
    esc.writeMicroseconds(2000);
    delay(2000);
    esc.writeMicroseconds(1000);
    delay(2000);
    esc.writeMicroseconds(1500);
    delay(1000);
}
