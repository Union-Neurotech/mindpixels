import time
import numpy as np
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

# Step 1: Initialize Board
def initialize_board():
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
    board.prepare_session()
    return board

# Step 2: Stream Data with Markers
def stream_data_with_markers(board:BoardShim, num_chunks:int=10, timesleep:int=1):
    board.start_stream()
    for i in range(num_chunks):
        time.sleep(timesleep)
        board.insert_marker(i + 1)  # Marker value increases with time
    board.stop_stream()

# Step 3: Get Data
def get_data(board:BoardShim):
    data = board.get_board_data()
    board.release_session()
    return data

# Step 4: Find Markers in Data
def find_markers(data, board:BoardShim):
    # marker_channel = data[-1, :]  # Markers in the last channel
    marker_channel = data[board.get_marker_channel(board.board_id)]  # Markers in the last channel
    marker_indices = [i for i, marker in enumerate(marker_channel) if marker != 0]
    return marker_indices, marker_channel

# Helper: Average EEG Channels Together
def average_channels(eeg_data, channel_indices):
    selected_channels = eeg_data[channel_indices, :]  # Select only the specified channels
    return np.mean(selected_channels, axis=0)  # Average across the selected channels

# Step 5: Split EEG Data at Marker Points, Averaging Selected Channels
def split_data_at_markers(data, marker_indices, eeg_channels_to_use):
    eeg_data = data[eeg_channels_to_use, :]  # Use only the specified EEG channels
    averaged_chunks = []

    # Loop through marker indices and split data into chunks
    start_idx = 0
    for idx in marker_indices:
        chunk = eeg_data[:, start_idx:idx]  # Get data from start to this marker for all selected channels
        averaged_chunk = average_channels(chunk, range(len(eeg_channels_to_use)))  # Average the channels
        averaged_chunks.append(averaged_chunk)  # Store the averaged chunk
        start_idx = idx  # Update the starting point for the next chunk

    # Add the remaining data after the last marker
    remaining_chunk = eeg_data[:, start_idx:]  # Get data after the last marker
    averaged_chunk = average_channels(remaining_chunk, range(len(eeg_channels_to_use)))
    averaged_chunks.append(averaged_chunk)
    
    return averaged_chunks

# Step 6: Display the Averaged Chunks
def display_averaged_chunks(averaged_chunks):
    for i, chunk in enumerate(averaged_chunks):
        plt.figure(figsize=(10, 4))
        plt.plot(chunk)
        plt.title(f'Averaged EEG Data Chunk {i + 1}')
        plt.xlabel('Sample Index')
        plt.ylabel('Averaged EEG Signal')
        plt.show()

if __name__ == "__main__":
# Main execution flow
    board = initialize_board()
    stream_data_with_markers(board)
    data = get_data(board)
    marker_indices, marker_channel = find_markers(data, board)

    # Specify EEG channels to average (example: channels 0, 1, and 2)
    eeg_channels_to_use = [0, 1, 2]

    # Split and average the EEG data across the specified channels
    averaged_chunks = split_data_at_markers(data, marker_indices, eeg_channels_to_use)

    # Display the averaged chunks of data
    display_averaged_chunks(averaged_chunks)
