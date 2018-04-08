class Session(object):
    """
    Creates session objects
    """
    def __init__(self, **kwargs):
        self.inactivity_period = kwargs.pop('inactivity_period')
        self.ip_address = kwargs.pop('ip_address')
        self.start_time = kwargs.pop('start_time')
        self.end_time = self.start_time
        self._webpage_requests = kwargs.pop('webpage_requests', 0)

    @property
    def _duration(self):
        return (self.end_time - self.start_time).total_seconds()

    def update_end_time(self, latest_request_time):
        """
        With each web request for this session, we update the end_time and increment our count
        """
        self.end_time = latest_request_time
        self._webpage_requests += 1

    def is_expired(self, current_time):
        """
        The domain logic of closing a session is enforced here
        """
        return (current_time - self.end_time).total_seconds() >= self.inactivity_period

    def __str__(self):
        """
        This returns a nice string representation of the session
        and can seamlessly be used for outputting into a file
        """
        return '{0},{1},{2},{3},{4}'.format(self.ip_address, self.start_time,
            self.end_time, self._duration, self._webpage_requests)
