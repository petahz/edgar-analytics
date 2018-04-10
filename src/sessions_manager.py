import csv
import logging

from collections import OrderedDict
from datetime import datetime
from session import Session


class SessionsManager(object):
    def __init__(self, **kwargs):
        """
        On initialization, we read our inactivity file 
        to determine the period metric by which we open and close sessions,
        and set input/output file paths as well as a time for the manager to track
        """
        self.input_csv_file_path = kwargs.pop('input_csv_file_path')
        self.inactivity_file_path = kwargs.pop('inactivity_file_path')
        self.output_sessions_file_path = kwargs.pop('output_sessions_file_path')
        self.last_recorded_time = None

        with open(self.inactivity_file_path, 'r') as inactivity_file:
            inactivity_value = inactivity_file.readline()
            try:
                self.inactivity_period = int(inactivity_value)
            except ValueError:
                raise Exception('The value provided in the inactivity period file cannot be parsed correctly.')
        
        self.current_sessions = OrderedDict()

    def open_stream(self):
        """
        Open stream reading in log csv file and creating or updating sessions
        """
        with open(self.input_csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                try:
                    user_ip_address = row['ip']
                    current_time = datetime.strptime('{0} {1}'.format(row['date'], row['time']), '%Y-%m-%d %H:%M:%S')
                except KeyError:
                    logging.warning('Row {0} missing necessary ip address identifier or datetime information to '
                                    'determine session intervals. Skipping over.'.format(idx + 1))
                    continue

                if user_ip_address not in self.current_sessions:
                    # Create a new session for this user
                    self.current_sessions[user_ip_address] = Session(**{
                        'inactivity_period': self.inactivity_period,
                        'ip_address': user_ip_address,
                        'start_time': current_time,
                    })
                else:
                    # A session exists for this user
                    # Update the end time of the session
                    # If time has lapsed, close inactive sessions
                    self.current_sessions[user_ip_address].update_end_time(current_time)
                
                if current_time != self.last_recorded_time:
                    self.last_recorded_time = current_time
                    self._close_sessions()

        # When the end of file is reached, we close out all remaining sessions
        self._close_sessions(close_all=True)
            
    def _close_sessions(self, close_all=False):
        """
        Go through all currently opened sessions and check if it is expired per the last
        webpage request time. If so, close the session and write to disk.
        """
        if close_all is True:
            closed_sessions = [session for _, session in
                self.current_sessions.items()]
            self.current_sessions = OrderedDict()
        else:
            closed_sessions = [session for _, session in self.current_sessions.items()
                               if session.is_expired(self.last_recorded_time)]
            for closed_session in closed_sessions:
                del self.current_sessions[closed_session.ip_address]
          
        with open(self.output_sessions_file_path, 'a') as output_file:
            for session in closed_sessions:
                output_file.write(str(session))
