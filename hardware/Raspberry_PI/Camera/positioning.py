import cv2
import numpy as np

def draw_crosshair(frame, center, size=20, color=(255, 0, 0), thickness=2):
    x, y = center
    cv2.line(frame, (x - size, y), (x + size, y), color, thickness)
    cv2.line(frame, (x, y - size), (x, y + size), color, thickness)

def main():
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Adjust the physical crosshair to the center of the camera view.")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and help with contour detection
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edged image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on area (consider only large contours)
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]

        if large_contours:
            # Get the largest contour (assuming it's the crosshair)
            largest_contour = max(large_contours, key=cv2.contourArea)

            # Get the center of the contour using the moments
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                draw_crosshair(frame, center)
                
                # Check the position of the crosshair and provide instructions
                if center[0] < frame.shape[1] // 2:
                    print("Move the crosshair to the right.")
                elif center[0] > frame.shape[1] // 2:
                    print("Move the crosshair to the left.")
                else:
                    print("Crosshair is close to the center horizontally. Adjust as needed.")

                if center[1] < frame.shape[0] // 2:
                    print("Move the crosshair down.")
                elif center[1] > frame.shape[0] // 2:
                    print("Move the crosshair up.")
                else:
                    print("Crosshair is close to the center vertically. Adjust as needed.")
                    
                    # You can define a threshold for the center and stop the program
                    if abs(center[0] - frame.shape[1] // 2) < 10 and abs(center[1] - frame.shape[0] // 2) < 10:
                        print("Crosshair is at the center. Stopping the program.")
                        break

        cv2.imshow("Camera Livestream", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
