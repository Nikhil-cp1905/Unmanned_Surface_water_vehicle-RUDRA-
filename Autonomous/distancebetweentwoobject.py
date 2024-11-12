import cv2
import numpy as np

def capture_frames(cam):
    ret1, frame1 = cam.read()
    if not ret1:
        print("Error capturing first frame.")
        return None, None

    cv2.waitKey(50)
    ret2, frame2 = cam.read()
    if not ret2:
        print("Error capturing second frame.")
        return None, None

    frame2 = cv2.flip(frame2, 1)
    return frame1, frame2

def detect_features(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    return keypoints1, descriptors1, keypoints2, descriptors2

def match_features(descriptors1, descriptors2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def calculate_distance(matches, baseline, focal_length):
    disparities = [match.distance for match in matches]
    average_disparity = np.mean(disparities) if disparities else 0

    if average_disparity == 0:
        return None

    distance_meters = (focal_length * baseline) / average_disparity
    distance_mm = distance_meters * 1000
    return distance_mm

def main():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Camera not accessible.")
        return

    baseline = 25.4
    focal_length = float(input("Enter the focal length in pixels: "))

    while True:
        img1, img2 = capture_frames(cam)
        if img1 is None or img2 is None:
            break

        keypoints1, descriptors1, keypoints2, descriptors2 = detect_features(img1, img2)
        matches = match_features(descriptors1, descriptors2)

        distance_mm = calculate_distance(matches, baseline, focal_length)
        
        img_matches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        
        if distance_mm is not None:
            text = f"Estimated Distance: {distance_mm:.2f} mm"
        else:
            text = "Unable to calculate distance"
        
        cv2.putText(img_matches, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Distance Estimation (mm)", img_matches)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

