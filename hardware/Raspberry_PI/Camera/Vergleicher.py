import cv2
from skimage.metrics import structural_similarity as ssim

def capture_image_from_camera():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    capture.release()
    return frame

def compare_images(reference_image, captured_image):
    # Convert images to grayscale
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    gray_captured = cv2.cvtColor(captured_image, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    similarity_index, _ = ssim(gray_reference, gray_captured, full=True)
    similarity_percentage = similarity_index * 100

    print(f"SSIM: {similarity_percentage:.2f}%")

    # Show the reference and captured images
    cv2.imshow("Reference Image", gray_reference)
    cv2.imshow("Captured Image", gray_captured)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Capture a reference image from the camera
    reference_image = capture_image_from_camera()

    # Capture an image to be compared from the camera
    captured_image = capture_image_from_camera()

    # Call the function to compare images
    compare_images(reference_image, captured_image)
