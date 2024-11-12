import cv2
import numpy as np

# Example calibration data
# Known purple intensity values and corresponding protein concentrations
intensity_data = np.array([50, 100, 150, 200, 250])  # Example intensity values
concentration_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # Corresponding concentrations in mg/mL

# Calculate the slope and intercept for the linear relationship
slope, intercept = np.polyfit(intensity_data, concentration_data, 1)

def detect_protein_concentration(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return None

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for purple color (positive biuret test)
    lower_purple = np.array([125, 50, 50])  # Lower bound of purple hue
    upper_purple = np.array([165, 255, 255])  # Upper bound of purple hue

    # Create a mask for purple regions
    mask = cv2.inRange(hsv_image, lower_purple, upper_purple)
    
    # Calculate the mean purple intensity in the detected region
    purple_pixels = cv2.mean(hsv_image, mask=mask)[0]  # Mean hue value for purple region
    
    # Estimate concentration using the slope and intercept
    estimated_concentration = slope * purple_pixels + intercept
    
    # Calculate the percentage of purple pixels in the image
    purple_ratio = cv2.countNonZero(mask) / (image.shape[0] * image.shape[1]) * 100  # Convert to percentage

    # Display results based on purple ratio
    if purple_ratio > 5:  # Adjust threshold as necessary
        print(f"Protein detected (positive biuret test): {purple_ratio:.2f}% of image area.")
    else:
        print(f"No significant protein detected (negative biuret test): {purple_ratio:.2f}% of image area.")
    
    print(f"Estimated protein concentration: {estimated_concentration:.2f} mg/mL")
    
    # Create a grayscale mask for visualization
    mask_grayscale = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Convert single channel to BGR for display

    # Display original image and the grayscale mask side by side
    combined_display = np.hstack((image, mask_grayscale))  # Combine images horizontally

    # Show the frames
    cv2.imshow("Original and Detected Protein Regions", combined_display)
    
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return estimated_concentration

# Test the function
image_path = '/home/nikhil/USWV/USV/sensors/protien.png'
detect_protein_concentration(image_path)

