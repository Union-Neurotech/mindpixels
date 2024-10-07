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
available_boards = ["Unicorn", "Cyton 8-Channel", "Cyton 16-Channel"]

# Dropdown for selecting the board
selected_board = st.selectbox("Select a Board to Connect", available_boards)

our_eeg_device  = None
done_processing = False

# Create a button to connect
if st.button("Connect"):
    boardID = get_boardID(selected_board)
    our_eeg_device = connect(boardID=boardID)
    st.write("Connected to EEG device.")

if our_eeg_device != None:
    # Status display (could be an input field or updated status text)
    status_display = st.text_input("Status Display", value="No active processes")


    if st.button("Start"):

        with st.status(label="Starting Data Stream", expanded=True):
            our_eeg_device.start_stream()
            st.write("Starting OpenCV image presentation...")
            # Simulate OpenCV image presentation in fullscreen
            run_opencv_presentation()
            # Once done, update status and return to UI
            our_eeg_device.stop_stream()
            st.write("Processing complete.")
            done_processing = True

    if done_processing:  
        # Placeholder for video/image processing section
        st.text_area("When process is done, the image overlay closes, and we return to the UI where your video/image is either processing or ready.")

        with st.status("Generating Image"):
            st.write("Parsing patterns")
            time.sleep(1)
            st.write("Propating Image net")
            time.sleep(1)
            st.write("Transcribing Dreams...")

        

