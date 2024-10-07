import streamlit as st
from comms import get_boardID, connect
from present import run_opencv_presentation
import time

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

# Dropdown for selecting the board
selected_board = st.selectbox("Select a Board to Connect", available_boards)

# Create a button to connect
if st.button("Connect"):
    boardID = get_boardID(selected_board)
    st.session_state.our_eeg_device = connect(boardID=boardID)
    # our_eeg_device = connect(boardID=boardID)
    st.write("Connected to EEG device.")

# Check if the EEG device is connected
if st.session_state.our_eeg_device is not None:
    # Status display (could be an input field or updated status text)
    status_display = st.text_input("Status Display", value="No active processes")

    st.info("Board is still connected, you can stream data by running START")
    
    if st.button("Start"):

        with st.status(label="Starting Data Stream", expanded=True):
            st.session_state.our_eeg_device.start_stream()
            st.write("Starting OpenCV image presentation...")
            # Simulate OpenCV image presentation in fullscreen
            run_opencv_presentation()
            # Stop the stream after presentation
            st.session_state.our_eeg_device.stop_stream()
            st.write("Processing complete.")
            st.session_state.done_processing = True

# Display processing section if done
if st.session_state.done_processing: 
        # Placeholder for video/image processing section
        st.text_area("When process is done, the image overlay closes, and we return to the UI where your video/image is either processing or ready.")

        with st.status("Generating Image"):
            st.write("Parsing patterns")
            time.sleep(1)
            st.write("Propating Image net")
            time.sleep(1)
            st.write("Transcribing Dreams...")


        if st.button("disconnect"):
            st.session_state.our_eeg_device.release_session()
            st.session_state.done_processing = False

        

