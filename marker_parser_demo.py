
import time
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
def stream_data_with_markers(board, duration=10):
    board.start_stream()
    for i in range(duration):
        time.sleep(1)
        board.insert_marker(i + 1)
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

# Step 5: Split EEG Data at Marker Points
def split_data_at_markers(data, marker_indices):
    eeg_data = data[0, :]  # Assuming we are working with the first EEG channel for now
    chunks = []
    
    # Loop through marker indices and split data into chunks
    start_idx = 0
    for idx in marker_indices:
        chunk = eeg_data[start_idx:idx]  # Get data from last marker (or start) to this marker
        chunks.append(chunk)  # Store the chunk
        start_idx = idx  # Update the starting point for the next chunk
    
    # Add the remaining data after the last marker
    chunks.append(eeg_data[start_idx:])
    
    return chunks

# Step 6: Display the chunks
def display_chunks(chunks):
    for i, chunk in enumerate(chunks):
        plt.figure(figsize=(10, 4))
        plt.plot(chunk)
        plt.title(f'EEG Data Chunk {i + 1}')
        plt.xlabel('Sample Index')
        plt.ylabel('EEG Signal')
        plt.show()

# Main execution flow
board = initialize_board()
stream_data_with_markers(board)
data = get_data(board)
marker_indices, marker_channel = find_markers(data, board)

# Split the EEG data into chunks
chunks = split_data_at_markers(data, marker_indices)

# Display the split chunks of data
display_chunks(chunks)