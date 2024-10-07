import streamlit as st
from comms import get_boardID, connect, disconnect
from present import run_opencv_presentation
import time
from ranking import rank_images
from proompter import rankings2images
def write_center_txt(text="default", type="h1"):
    st.markdown(f"<{type} style='text-align: center; color: white;'>{text}</{type}>", 
                unsafe_allow_html=True)
    

write_center_txt(text="MINDPIXELS")
write_center_txt(text="Generate moving images with your MIND!", type="h3")


# Define available boards (for demonstration purposes)
available_boards = ["Synthetic", "Unicorn", "Cyton 8-Channel", "Cyton 16-Channel"]

# Initialize session state for EEG device and processing status
if "our_eeg_device" not in st.session_state:
    st.session_state.our_eeg_device = None

if "done_processing" not in st.session_state:
    st.session_state.done_processing = False

if "selected_board" not in st.session_state:
    st.session_state.selected_board = None

# Dropdown for selecting the board

if st.session_state.selected_board is None:
    selected_board = st.selectbox("Select a Board to Connect", available_boards)
    # Create a button to connect
    if st.button("Connect"):
        boardID = get_boardID(selected_board)
        st.session_state.our_eeg_device = connect(boardID=boardID)
        st.session_state.selected_board = selected_board  # Store the selected board in session state
        st.write(f"Connected to {selected_board}.")
else:
    st.write(f"Connected to {st.session_state.selected_board}.")

# Check if the EEG device is connected
if st.session_state.our_eeg_device is not None:
    # Status display (could be an input field or updated status text)
    status_display = st.text_input("Status Display", value="No active processes")

    st.info("Board is still connected, you can stream data by running START")

    if st.button("Start"):

        with st.status(label="Starting Data Stream", expanded=True):
            st.write("Starting OpenCV image presentation...")
            # Simulate OpenCV image presentation in fullscreen
            data, st.session_state.our_eeg_device = run_opencv_presentation(board=st.session_state.our_eeg_device, 
                                                                      image_folder='assets/', 
                                                                      display_time=2) # board should start stream in here
            # Stop the stream after presentation
            st.write("Now Processing")
            boardID_local = st.session_state.our_eeg_device.board_id

            # PROCESS THE DATA RANK IT
            sorted_indexes_list, sorted_ranks_dict, index_of_images, sorted_images_by_rank = rank_images(images_dir = "assets/", 
                                                                                                        data    = data, 
                                                                                                        board   = st.session_state.our_eeg_device, 
                                                                                                        boardID = boardID_local, 
                                                                                                        eeg_channels_to_use = st.session_state.our_eeg_device.get_eeg_channels(boardID_local))
            
            if len(sorted_images_by_rank) > 5:
                best_of = sorted_images_by_rank[0:5]
            else:
                best_of = sorted_images_by_rank
                
            st.info(f"Best five images are {best_of}")
            st.write("Processing complete.")

            st.session_state.done_processing = True

# Display processing section if done
if st.session_state.done_processing: 
        # Placeholder for video/image processing section
        st.info("When process is done, the image overlay closes, and we return to the UI where your video/image is either processing or ready.")

        with st.status("Generating Image"):
            st.write("Processing Request")
            final_image_path = rankings2images(best_of)
            st.write("Propating Image net")
            st.write("Disconnecting from Board")
            st.session_state.our_eeg_device.release_session()

            st.info("Please REFRESH (CTRL-R) to connect and stream again.")

        

