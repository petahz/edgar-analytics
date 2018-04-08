import sys

from sessions_manager import SessionsManager


class Sessionization(object):
    """
    Sessionization app with provided file path arguments and a SessionsManager
    """
    def __init__(self):
        if sys.argv[3] is None:
            raise Exception('3 arguments for input, inactivity, and the text file to \
                output need to be provided.')

        sessions_manager = SessionsManager(**{
            'input_csv_file_path': sys.argv[1],
            'inactivity_file_path': sys.argv[2],
            'output_sessions_file_path': sys.argv[3],
        })

        sessions_manager.open_stream()


if __name__ == '__main__':
    Sessionization()
