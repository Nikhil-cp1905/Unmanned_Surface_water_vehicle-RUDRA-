#include <IBusBM.h>

IBusBM ibusRc;

HardwareSerial& ibusRcSerial = Serial1;
HardwareSerial& debugSerial = Serial;

const int motorLeftPin = 9;   // Define PWM pin for left motor
const int motorRightPin = 10;  // Define PWM pin for right motor

void setup() {
  debugSerial.begin(74880);
  ibusRc.begin(ibusRcSerial);
  
  pinMode(motorLeftPin, OUTPUT);
  pinMode(motorRightPin, OUTPUT);
}

// Read the channel and map it to a desired range.
// If the channel is off, return the default value
int readChannel(byte channelInput, int minLimit, int maxLimit, int defaultValue){
  uint16_t ch = ibusRc.readChannel(channelInput);
  if (ch < 100) return defaultValue;
  return map(ch, 1000, 2000, minLimit, maxLimit);
}

// Control motor speed based on interpolated values
void controlMotors(int throttle, int steering) {
  int leftMotorSpeed, rightMotorSpeed;

  // Turning logic: steer channel affects which motor is active
  if (steering > 10) { // Turn right, reduce left motor speed
    leftMotorSpeed = throttle;
    rightMotorSpeed = 0;
  } else if (steering < -10) { // Turn left, reduce right motor speed
    leftMotorSpeed = 0;
    rightMotorSpeed = throttle;
  } else { // Go straight
    leftMotorSpeed = throttle;
    rightMotorSpeed = throttle;
  }

  // Map throttle values to PWM (0-255 for analogWrite)
  analogWrite(motorLeftPin, map(leftMotorSpeed, -100, 100, 0, 255));
  analogWrite(motorRightPin, map(rightMotorSpeed, -100, 100, 0, 255));
}

void loop() {
  // Channel 2 for throttle (forward/reverse), Channel 1 for steering (left/right)
  int throttle = readChannel(1, -100, 100, 0); // Adjust for your throttle channel
  int steering = readChannel(0, -100, 100, 0); // Adjust for your steering channel

  // Control motor speeds based on throttle and steering
  controlMotors(throttle, steering);

  // Debug output
  debugSerial.print("Throttle: ");
  debugSerial.print(throttle);
  debugSerial.print(" Steering: ");
  debugSerial.println(steering);

  delay(10);
}
