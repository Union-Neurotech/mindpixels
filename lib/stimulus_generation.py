import cv2
import numpy as np

# Get screen dimensions
screen_width = 1920
screen_height = 1080

# Create a black image
black_image = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Create a window named 'display'
cv2.namedWindow('display', cv2.WINDOW_NORMAL)
cv2.resizeWindow('display', screen_width, screen_height)

# Move the window to the center of the screen
cv2.moveWindow('display', 100, 50)

# Set the window to full screen
cv2.setWindowProperty('display', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Display the black image
cv2.imshow('display', black_image)

# Wait for a key press
cv2.waitKey(0)
cv2.destroyAllWindows()
