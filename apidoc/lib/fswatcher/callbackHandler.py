class CallbackHandler():

    """Handle FileSystem msodifications to refresh documentation
    """
    def __init__(self, callback):
        self.callback = callback

    def on_change(self, event):
        """Default handler
        """
        self.callback(event)
