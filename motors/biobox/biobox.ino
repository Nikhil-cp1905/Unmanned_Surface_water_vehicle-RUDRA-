// Pin definitions
const int pumpMotorPin = 9;   // Pin for the water pump motor
const int rotationMotorPin = 10; // Pin for the bio box rotation motor

// Timing and cycle variables
const unsigned long pumpDuration = 5000;  // Pump for 5 seconds
const unsigned long rotationDuration = 2000; // Rotate for 2 seconds
const int totalCycles = 5; // Total number of cycles
int currentCycle = 0; // Track the current cycle

void setup() {
    pinMode(pumpMotorPin, OUTPUT);
    pinMode(rotationMotorPin, OUTPUT);
    Serial.begin(9600); // Initialize serial communication for debugging
}

void loop() {
    if (currentCycle < totalCycles) {
        // Pump water
        Serial.println("Starting water pump...");
        digitalWrite(pumpMotorPin, HIGH); // Turn on the pump
        delay(pumpDuration); // Wait for pumpDuration
        digitalWrite(pumpMotorPin, LOW); // Turn off the pump
        Serial.println("Water pump stopped.");

        // Rotate the bio box
        Serial.println("Rotating bio box...");
        digitalWrite(rotationMotorPin, HIGH); // Turn on the rotation motor
        delay(rotationDuration); // Wait for rotationDuration
        digitalWrite(rotationMotorPin, LOW); // Turn off the rotation motor
        Serial.println("Bio box rotation stopped.");

        currentCycle++; // Move to the next cycle
        Serial.print("Cycle completed: ");
        Serial.println(currentCycle);
    } else {
        // Stop the entire process after completing all cycles
        Serial.println("All cycles completed.");
        while (true); // Stop the loop
    }
}
