from scipy.signal import butter, filtfilt, find_peaks
from scipy.integrate import simpson
import numpy as np

from brainflow import BoardIds, BoardShim
from marker_parser import initialize_board, stream_data_with_markers, get_data, find_markers, average_channels

# Helper: Bandpass Filter (Butterworth)
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')

    # filtfilt requires that the input length be greater than 3 times the filter order
    padlen = 3 * max(len(b), len(a))
    
    # Check if the data is long enough to be filtered
    if len(data) <= padlen:
        print("Warning: Chunk too short for filtering, skipping filtering step.")
        return data  # Return the unfiltered data
    
    return filtfilt(b, a, data)


# Helper: Analyze P300 waveform characteristics
def analyze_p300_waveform(chunk, fs):
    # Step 1: Bandpass filter the chunk to isolate P300 frequencies (0.5 - 8 Hz)
    filtered_chunk = bandpass_filter(chunk, 0.5, 8, fs)

    # Step 2: Extract the P300 time window (250-500 ms)
    start_sample = int(0.25 * fs)  # 250 ms
    end_sample = int(0.5 * fs)     # 500 ms
    chunk_window = filtered_chunk[start_sample:end_sample]

    # Step 3: Detect positive peaks within the time window
    peaks, properties = find_peaks(chunk_window, height=0)  # Find positive peaks

    if len(peaks) == 0:
        return None  # No P300 detected

    # Step 4: Analyze the characteristics of the P300 peak
    peak_amplitude = properties["peak_heights"].max()  # Maximum amplitude of the peak
    peak_index = peaks[properties["peak_heights"].argmax()]  # Index of the peak

    # Step 5: Area Under the Curve (AUC) for the P300 segment
    auc = simpson(chunk_window, dx=1/fs)  # Use Simpson's rule to calculate AUC

    # Step 6: Root Mean Square (RMS) Power of the P300
    rms_power = np.sqrt(np.mean(np.square(chunk_window)))

    return {
        "peak_amplitude": peak_amplitude,
        "peak_index": peak_index,
        "auc": auc,
        "rms_power": rms_power
    }

# Step 5: Split EEG Data at Marker Points, Analyze P300 Characteristics
def split_data_and_analyze_p300s(data, marker_indices, eeg_channels_to_use, fs):
    eeg_data = data[eeg_channels_to_use, :]  # Use only the specified EEG channels
    averaged_chunks = []
    p300_analysis_results = []

    # Loop through marker indices and split data into chunks
    start_idx = 0
    for idx in marker_indices:
        chunk = eeg_data[:, start_idx:idx]  # Get data from start to this marker for all selected channels
        averaged_chunk = average_channels(chunk, range(len(eeg_channels_to_use)))  # Average the channels
        averaged_chunks.append(averaged_chunk)  # Store the averaged chunk

        # Step 6: Analyze P300 characteristics in the chunk
        p300_analysis = analyze_p300_waveform(averaged_chunk, fs)
        p300_analysis_results.append(p300_analysis)  # Store the P300 analysis result
        
        start_idx = idx  # Update the starting point for the next chunk

    # Add the remaining data after the last marker
    remaining_chunk = eeg_data[:, start_idx:]  # Get data after the last marker
    averaged_chunk = average_channels(remaining_chunk, range(len(eeg_channels_to_use)))
    averaged_chunks.append(averaged_chunk)
    
    # Analyze P300 in the last chunk
    p300_analysis = analyze_p300_waveform(averaged_chunk, fs)
    p300_analysis_results.append(p300_analysis)

    return averaged_chunks, p300_analysis_results

# Example of comparing P300s
def compare_p300s(p300_analysis_results):
    for i, result in enumerate(p300_analysis_results):
        if result is None:
            print(f"Chunk {i + 1}: No P300 detected")
        else:
            print(f"Chunk {i + 1}:")
            print(f"  Peak Amplitude: {result['peak_amplitude']:.2f} µV")
            print(f"  Area Under Curve (AUC): {result['auc']:.2f}")
            print(f"  RMS Power: {result['rms_power']:.2f} µV")
            print()

if __name__ == "__main__":
    # Main execution flow
    board = initialize_board()
    stream_data_with_markers(board, num_chunks=10, timesleep=3)
    data = get_data(board)
    marker_indices, marker_channel = find_markers(data, board)

    # Specify EEG channels to average (example: channels 0, 1, and 2)
    eeg_channels_to_use = [0, 1, 2]
    fs = BoardShim.get_sampling_rate(BoardIds.SYNTHETIC_BOARD.value)  # Sampling rate of the board

    # Split and average the EEG data across the specified channels, and analyze P300 characteristics
    averaged_chunks, p300_analysis_results = split_data_and_analyze_p300s(data, marker_indices, eeg_channels_to_use, fs)

    # Compare P300 results
    compare_p300s(p300_analysis_results)