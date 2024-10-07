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
def get_data(board):
    data = board.get_board_data()
    board.release_session()
    return data

# Step 4: Find Markers in Data
def find_markers(data):
    # marker_channel = data[-1, :]  # Markers in the last channel
    marker_channel = data[board.get_marker_channel(board.board_id)]  # Markers in the last channel
    marker_indices = [i for i, marker in enumerate(marker_channel) if marker != 0]
    return marker_indices, marker_channel

# Step 5: Plot Data with Markers
def plot_data_with_markers(data, marker_indices, marker_channel):
    eeg_channel = data[0, :]  # First EEG channel for demonstration
    plt.figure(figsize=(10, 6))
    plt.plot(eeg_channel, label='EEG Data')
    plt.scatter(marker_indices, marker_channel[marker_indices], color='red', label='Markers')
    plt.legend()
    plt.title('EEG Data with Markers')
    plt.show()

def plot_data_with_marker_lines(data, marker_indices, marker_channel):
    eeg_channel = data[0, :]  # First EEG channel for demonstration

    plt.figure(figsize=(10, 6))
    plt.plot(eeg_channel, label='EEG Data')

    # Plot vertical lines for each marker
    for idx in marker_indices:
        plt.axvline(x=idx, color='red', linestyle='--', label='Marker' if idx == marker_indices[0] else "")

    plt.legend()
    plt.title('EEG Data with Markers (Vertical Lines)')
    plt.xlabel('Sample Index')
    plt.ylabel('EEG Signal')
    plt.show()

def plot_data_with_variable_marker_lines(data, marker_indices, marker_channel):
    eeg_channel = data[0, :]  # First EEG channel for demonstration

    plt.figure(figsize=(10, 6))
    plt.plot(eeg_channel, label='EEG Data')

    # Plot vertical lines for each marker with height based on marker amplitude
    for idx in marker_indices:
        # Get the height from the marker channel, use it to set the line's top
        plt.vlines(x=idx, ymin=min(eeg_channel), ymax=marker_channel[idx], color='red', linestyle='--', label='Marker' if idx == marker_indices[0] else "")

    plt.legend()
    plt.title('EEG Data with Markers of Variable Height')
    plt.xlabel('Sample Index')
    plt.ylabel('EEG Signal')
    plt.show()

# Main execution flow
board = initialize_board()
stream_data_with_markers(board)
data = get_data(board)
marker_indices, marker_channel = find_markers(data, board)
# plot_data_with_markers(data, marker_indices, marker_channel)
plot_data_with_marker_lines(data, marker_indices, marker_channel)
# plot_data_with_variable_marker_lines(data, marker_indices, marker_channel)
