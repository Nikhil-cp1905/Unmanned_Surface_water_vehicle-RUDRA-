from gpiozero import MCP3008
import time

# Constants
VREF = 5000            # Reference voltage in mV
ADC_RES = 1024         # ADC Resolution
READ_TEMP = 25         # Temperature in °C
CAL1_V = 131           # Calibration voltage at 25°C
CAL1_T = 25            # Calibration temperature in °C
CAL2_V = 1300          # Calibration voltage at 15°C
CAL2_T = 15            # Second calibration temperature in °C
TWO_POINT_CALIBRATION = 0

# Dissolved Oxygen Table
DO_Table = [
    14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
    11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270,
    9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,
    7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410
]

# Initialize the ADC (MCP3008 on channel 0 for DO sensor input)
adc = MCP3008(channel=0)

# Function to calculate DO, similar to the Arduino readDO function
def readDO(voltage_mv, temperature_c):
    if TWO_POINT_CALIBRATION == 0:
        V_saturation = CAL1_V + 35 * (temperature_c - CAL1_T)
    else:
        V_saturation = ((temperature_c - CAL2_T) * (CAL1_V - CAL2_V) / (CAL1_T - CAL2_T)) + CAL2_V
    do_value = (voltage_mv * DO_Table[temperature_c] / V_saturation)
    return do_value

# Main loop to read from the sensor and calculate DO
try:
    while True:
        adc_raw = adc.value * ADC_RES                   # Get ADC reading (0-1), scale to 0-1023
        adc_voltage = VREF * adc_raw / ADC_RES          # Calculate ADC voltage in mV
        temperature = READ_TEMP                         # Use fixed or measured temperature
        do_value = readDO(adc_voltage, temperature)     # Calculate DO

        # Output data
        print(f"Temperature: {temperature} °C")
        print(f"ADC RAW: {int(adc_raw)}")
        print(f"ADC Voltage: {adc_voltage:.2f} mV")
        print(f"DO: {do_value / 1000:.2f} mg/L\n")     # Display DO in mg/L

        time.sleep(1)  # Read sensor every second
except KeyboardInterrupt:
    print("Program terminated.")
