import cv2
import os
import random
from brainflow import BoardShim, BrainFlowInputParams
import numpy as np

# Edit path to image folder
dir = "assets/"

def run_opencv_presentation(board:BoardShim, image_folder:str="images/", display_time:int=2, screen_resolution=(1920, 1080)):
    """
    Displays images in fullscreen with markers and returns EEG data.
    
    Parameters:
    - board: EEG board object (for streaming data and inserting markers).
    - image_folder: Path to the folder containing images.
    - display_time: Time (in seconds) each image should be displayed.
    
    Returns:
    - EEG data collected during the session.
    - the board you passed in
    """
    # Get list of image files from the specified folder
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if image_files == []: print("NO IMAGE FILES, did you remember to add them?")

    # Sort the images to ensure a specific order if needed
    image_files.sort()

    # Create a fullscreen window for OpenCV
    window_name = "Image Presentation"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Start the EEG stream (assuming the stream is not already started)
    board.start_stream()

    for idx, image_file in enumerate(image_files):
        # Load the image and resize to fit fullscreen (assuming 1920x1080 for simplicity)
        img = cv2.imread(image_file)
        # img = cv2.resize(img, (1920, 1080))

        # Get the dimensions of the image and the screen
        img_height, img_width = img.shape[:2]
        screen_width, screen_height = screen_resolution

        # Create a black background (same size as the screen resolution)
        background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

        x_offset = (background.shape[1] - img.shape[1]) // 2
        y_offset = (background.shape[0] - img.shape[0]) // 2
        
        
        # Ensure the image fits within the screen dimensions
        if img_width <= screen_width and img_height <= screen_height:
            # Place the image on the black background at the calculated offset
            background[y_offset:y_offset + img_height, x_offset:x_offset + img_width] = img
        else:
            # If the image is larger than the screen, resize it to fit while maintaining aspect ratio
            img = cv2.resize(img, (screen_width, screen_height), interpolation=cv2.INTER_AREA)
            background = img  # Use the resized image directly as the background
        
        marker = idx + 1  # Marker could be any value; using image index here
        # Insert a marker into the EEG stream
        print(f'Inserting Marker for image {idx} ({image_file})')
        board.insert_marker(marker)
        # Display the image
        cv2.imshow(window_name, background)

        # Wait for the specified display time
        cv2.waitKey(display_time * 1000)

    # Stop the stream and close the OpenCV window
    board.stop_stream()
    cv2.destroyAllWindows()

    # Get and return the EEG data
    data = board.get_board_data()
    return data, board

def run_opencv_presentation_lite(count=50):
    used = set()
    images = os.listdir(dir)
    for i in range(count):

        # Get random non duplicated image
        idx = random.randint(0, len(images)-1)
        while idx in used:
            idx = random.randint(0, len(images)-1)   
        used.add(idx)         
        img = images[idx]
        path = os.path.join(dir, img)
        print(path)
        image = cv2.imread(path)

        # Insert marker

        # Show the image and wait for 1 second
        cv2.imshow("image", image)
        cv2.waitKey(1000)

if __name__ == "__main__":
    # run_opencv_presentation_lite(3)

    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board = BoardShim(-1, params)
    board.prepare_session()
    data, board = run_opencv_presentation(board, "assets/", 1)
    board.release_session()