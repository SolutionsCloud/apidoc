import os
import time
import threading

from .event import Event


class Observer(threading.Thread):
    """Observe change in file FileSystem
    """
    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.signatures = {}
        self.handlers = {}
        self.terminated = False

    def add_handler(self, path, handler):
        """Add a path in watch queue
        """
        self.signatures[path] = self.get_path_signature(path)
        self.handlers[path] = handler

    def get_path_signature(self, path):
        """generate a unique signature for file contained in path
        """
        if not os.path.exists(path):
            return None
        if os.path.isdir(path):
            merge = {}
            for root, dirs, files in os.walk(path):
                for name in files:
                    full_name = os.path.join(root, name)
                    merge[full_name] = os.stat(full_name)
            return merge
        else:
            return os.stat(path)

    def check(self):
        """Check if a file is changed
        """
        for (path, handler) in self.handlers.items():
            current_signature = self.signatures[path]
            new_signature = self.get_path_signature(path)
            if new_signature != current_signature:
                self.signatures[path] = new_signature
                handler.on_change(Event(path))

    def run(self):
        """Main loop of observer's thread. looks for changes in one of paths and call on_change of EventHandler
        """
        while not self.terminated:
            self.check()
            time.sleep(0.2)

    def stop(self):
        """Stop thread loop
        """
        self.terminated = True
