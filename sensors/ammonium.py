import cv2
import numpy as np

# Example calibration data for Nessler's reagent test
# Known intensity values and corresponding ammonium concentrations
intensity_data = np.array([50, 100, 150, 200, 250])  # Example intensity values (may vary)
concentration_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # Corresponding concentrations in mg/mL

# Calculate the slope and intercept for the linear relationship
slope, intercept = np.polyfit(intensity_data, concentration_data, 1)

def detect_yellow_color(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found.")
        return None

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define a broader HSV range for yellow colors
    # This range includes various shades of yellow
    lower_yellow = np.array([20, 100, 100])  # Lower bound for yellow hue
    upper_yellow = np.array([30, 255, 255])  # Upper bound for yellow hue

    # Create a mask for yellow regions
    mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # Use morphological operations to enhance the mask (remove noise)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours of the detected particles
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original image for visualization
    contour_image = image.copy()
    for contour in contours:
        if cv2.contourArea(contour) > 10:  # Filter small contours
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)

    # Calculate the mean intensity of detected yellow pixels
    mean_color_pixels = cv2.mean(hsv_image, mask=mask)[0]  # Mean hue value for detected yellow region
    
    # Estimate concentration using the slope and intercept
    estimated_concentration = slope * mean_color_pixels + intercept
    
    # Calculate the percentage of detected yellow pixels in the image
    yellow_ratio = cv2.countNonZero(mask) / (image.shape[0] * image.shape[1]) * 100  # Convert to percentage

    # Display results based on yellow ratio
    if yellow_ratio > 5:  # Adjust threshold as necessary
        print(f"Yellow color detected (positive test): {yellow_ratio:.2f}% of image area.")
    else:
        print(f"No significant yellow color detected (negative test): {yellow_ratio:.2f}% of image area.")
    
    print(f"Estimated ammonium concentration: {estimated_concentration:.2f} mg/mL")
    
    # Create a grayscale mask for visualization
    mask_grayscale = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Convert single channel to BGR for display

    # Display original image with contours and the grayscale mask side by side
    combined_display = np.hstack((contour_image, mask_grayscale))  # Combine images horizontally

    # Show the frames
    cv2.imshow("Original Image with Detected Yellow Regions and Mask", combined_display)
    
    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return estimated_concentration

# Test the function
image_path = '/home/nikhil/USWV/USV/sensors/nessler.png'  # Change to your image path
detect_yellow_color(image_path)
