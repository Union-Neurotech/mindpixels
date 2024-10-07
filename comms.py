import brainflow
from brainflow import BoardShim, BoardIds, BrainFlowInputParams

def get_boardID(label):
    available_boards = {
        "Unicorn": BoardIds.UNICORN_BOARD.value,
        "Cyton 8-Channel": BoardIds.CYTON_BOARD.value, 
        "Cyton 16-Channel": BoardIds.CYTON_DAISY_BOARD
    }
    if label in available_boards.keys():
        return available_boards[label]
    else:
        return BoardIds.SYNTHETIC_BOARD.value
        
def connect(boardID:int=BoardIds.SYNTHETIC_BOARD.value, serialPort:str='') -> BoardShim:
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board = BoardShim(boardID, params)
    board.prepare_session()
    return board

