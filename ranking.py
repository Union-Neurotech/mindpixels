from signal_processing import find_markers, split_data_and_analyze_p300s, compare_p300s
from brainflow import BoardShim, BoardIds, BrainFlowInputParams
from present import run_opencv_presentation
import os

def rank_images(images_dir, data, board:BoardShim, boardID:int, eeg_channels_to_use:list=[0, 1, 2]):
    """
    Ranks p300s by RMS power
    """
    marker_indices, marker_channel = find_markers(data, board)

    # Specify EEG channels to average (example: channels 0, 1, and 2)
    eeg_channels_to_use = eeg_channels_to_use
    fs = BoardShim.get_sampling_rate(boardID)  # Sampling rate of the board

    # Split and average the EEG data across the specified channels, and analyze P300 characteristics
    averaged_chunks, p300_analysis_results = split_data_and_analyze_p300s(data, marker_indices, eeg_channels_to_use, fs)

    p300_ranks = []
    p300_rank_dict = {}
    p300_idx_rank_dict = {}
    for i, result in enumerate(p300_analysis_results):
        if result != None:
            rank = round(result['rms_power'], 2)
        else:
            rank = 0.0
        p300_ranks.append(0.0)
        p300_rank_dict[i] = {'rank': rank}
        p300_idx_rank_dict[rank] = {'index': i}
    
    # Compare P300 results
    compare_p300s(p300_analysis_results)

    index_of_images = {}
    for i, img_name in enumerate(os.listdir(images_dir)):
        index_of_images[i] = img_name

    sorted_ranks   = {key: p300_idx_rank_dict[key] for key in sorted(p300_idx_rank_dict.keys())}
    sorted_indexes = []
    for rank in sorted_ranks.keys():
        sorted_indexes.append(sorted_ranks[rank]['index'])

    sorted_images_by_rank = []
    for i in sorted_indexes:
        # brief tweak - something about the remaining indexes sometimes reuslts in them being larger than there are images
        if i < len(sorted_indexes):
            sorted_images_by_rank.append(index_of_images[i])

    # sorted indexes are indexes in order of rank
    # sorted ranks is a dict of all ranks
    # index of images is all indexes and their associated images
    # sorted_images_by_rank is a list in descending order of best to worst images


    # images that dont appear had no p300
    return sorted_indexes, sorted_ranks, index_of_images, sorted_images_by_rank
    

if __name__ == "__main__":
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board = BoardShim(-1, params)
    board.prepare_session()
    data, board = run_opencv_presentation(board, "assets/", 1)

    sorted_indexes_list, sorted_ranks_dict, index_of_images, sorted_images_by_rank = rank_images(images_dir="assets/", data=data, board=board, boardID=board.board_id, eeg_channels_to_use=board.get_eeg_channels(board.board_id))


    board.release_session()
