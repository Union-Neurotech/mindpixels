import cv2
import numpy as np


def show_full_screen(image_path):
    # Get screen dimensions
    screen_width = 1920  # Replace with actual screen width
    screen_height = 1080  # Replace with actual screen height

    # Load the image
    img = cv2.imread(image_path)

    # Resize the image to fit the screen
    scale = min(screen_width / img.shape[1], screen_height / img.shape[0])
    new_size = (int(img.shape[1] * scale), int(img.shape[0] * scale))
    resized_img = cv2.resize(img, new_size)

    # Create a full screen window
    cv2.namedWindow("FullScreen", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("FullScreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Move the window to the center of the screen
    cv2.moveWindow("FullScreen", 0, 0)

    # Display the image
    cv2.imshow("FullScreen", resized_img)

    # Wait for a key press
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Usage
    show_full_screen('lib\space.jpg')