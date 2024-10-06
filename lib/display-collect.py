# For image and data collection
import cv2
import os

images_folder = 'images_folder'

# TO REMOVE, will be PIPED THROUGH =============
print("CONNECT TO BOARD")
print("SUCCESS")
# =============


# Function to display images
def display_images(image_paths):
    # Create fullscreen window
    screen_width = 1920  # Replace with actual screen width
    screen_height = 1080  # Replace with actual screen height
    
    # Set the window size to match the screen resolution
    cv2.namedWindow('Fullscreen', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Fullscreen', screen_width, screen_height)
    
    # Make the window fullscreen
    cv2.setWindowProperty('Fullscreen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Read the first image
    img = cv2.imread(image_paths[0])
    
    # Display each image in the loop
    for i in range(len(image_paths)):
        cv2.imshow('Fullscreen', img)
        
        # Wait for a key press
        key = cv2.waitKey(0)
        
        # If Esc is pressed, exit the loop
        if key == 27:
            break
        
        # Move to the next image
        img = cv2.imread(image_paths[(i + 1) % len(image_paths)])

if __name__ == "__main__":
    pass