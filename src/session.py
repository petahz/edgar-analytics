class Session():
    """
    Creates session objects
    """
    def __init__(self, **kwargs):
        self.ip_address = kwargs.pop('ip_address')
        self.start_time = kwargs.pop('start_time')
        self.end_time = kwargs.pop('end_time', None)
        self.duration = kwargs.pop('duration', 0)
        self.webpage_requests = kwargs.pop('webpage_requests', 0)

    def increment_duration(self):
        self.duration += 1

    def increment_webpage_requests(self):
        self.webpage_requests += 1

    def __str__(self):
        """
        This returns a nice string representation of the session
        and can seamlessly be used for outputting into a file
        """
        return '{0},{1},{2},{3},{4}'.format(self.ip_address, self.start_time, 
                        self.end_time, self.duration, self.webpage_requests)
