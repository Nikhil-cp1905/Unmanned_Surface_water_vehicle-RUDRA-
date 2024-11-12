import cv2
import numpy as np

# Example calibration data for browning detection
# Known intensity values and corresponding browning concentrations
intensity_data = np.array([50, 100, 150, 200, 250])  # Example intensity values (may vary)
concentration_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # Corresponding concentrations in mg/mL

# Calculate the slope and intercept for the linear relationship
slope, intercept = np.polyfit(intensity_data, concentration_data, 1)

def detect_browning_color(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return None

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for brown colors
    lower_brown = np.array([10, 100, 20])  # Lower bound for brown hue
    upper_brown = np.array([20, 255, 200])  # Upper bound for brown hue

    # Create a mask for brown regions
    mask = cv2.inRange(hsv_image, lower_brown, upper_brown)

    # Use morphological operations to enhance the mask (remove noise)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours of the detected brown regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original image for visualization
    contour_image = image.copy()
    for contour in contours:
        if cv2.contourArea(contour) > 10:  # Filter small contours
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)

    # Calculate the mean intensity of detected brown pixels
    mean_color_pixels = cv2.mean(hsv_image, mask=mask)[0]  # Mean hue value for detected region
    
    # Estimate concentration using the slope and intercept
    estimated_concentration = slope * mean_color_pixels + intercept
    
    # Calculate the percentage of detected brown pixels in the image
    brown_ratio = cv2.countNonZero(mask) / (image.shape[0] * image.shape[1]) * 100  # Convert to percentage

    # Display results based on brown ratio
    if brown_ratio > 5:  # Adjust threshold as necessary
        print(f"Browning color detected (positive test): {brown_ratio:.2f}% of image area.")
    else:
        print(f"No significant browning color detected (negative test): {brown_ratio:.2f}% of image area.")
    
    print(f"Estimated browning concentration: {estimated_concentration:.2f} mg/mL")
    
    # Create a grayscale mask for visualization
    mask_grayscale = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Convert single channel to BGR for display

    # Display original image with contours and the grayscale mask side by side
    combined_display = np.hstack((contour_image, mask_grayscale))  # Combine images horizontally

    # Show the frames
    cv2.imshow("Original Image with Detected Browning Regions and Mask", combined_display)
    
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return estimated_concentration

# Test the function
image_path = '/home/nikhil/USWV/USV/sensors/peroxide.png'  # Change to your image path
detect_browning_color(image_path)

