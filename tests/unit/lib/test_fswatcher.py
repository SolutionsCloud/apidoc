import unittest
import tempfile
import os
import time
import threading

from mock import MagicMock

from apidoc.lib.fswatcher.observer import Observer
from apidoc.lib.fswatcher.event import Event
from apidoc.lib.fswatcher.callbackHandler import CallbackHandler


class TestFsWatcher(unittest.TestCase):

    def stub_function_TestFsWatcher(event):
        pass

    def test_Event(self):
        result = Event("foo")
        self.assertEqual("foo", result.path)

    def test_callbackHandler(self):
        mock_function = MagicMock()

        handler = CallbackHandler(mock_function)
        handler.on_change("bar")

        mock_function.assert_called_once_with("bar")

    def test_observer_check(self):
        observer = Observer()
        mock_function1 = MagicMock()
        mock_function2 = MagicMock()
        with tempfile.TemporaryDirectory() as tmpdirname1:
            with tempfile.TemporaryDirectory() as tmpdirname2:
                observer.add_handler(tmpdirname1, CallbackHandler(mock_function1))
                observer.add_handler(tmpdirname2, CallbackHandler(mock_function2))
                open(os.path.join(tmpdirname1, 'file'), 'w').close()
                open(os.path.join(tmpdirname2, 'file'), 'w').close()
                observer.check()
                open(os.path.join(tmpdirname1, 'file2'), 'w').close()
                observer.check()

                self.assertEqual(2, len(mock_function1.mock_calls))
                self.assertEqual(1, len(mock_function2.mock_calls))

    def test_observer_nothingchanges(self):
        observer = Observer()
        mock_function = MagicMock()
        with tempfile.TemporaryDirectory() as tmpdirname:
            observer.add_handler(tmpdirname, CallbackHandler(mock_function))
            observer.check()

            self.assertEqual(0, len(mock_function.mock_calls))

    def test_observer_recurcive(self):
        observer = Observer()
        mock_function = MagicMock()
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.mkdir(os.path.join(tmpdirname, 'foo'))

            observer.add_handler(tmpdirname, CallbackHandler(mock_function))
            open(os.path.join(tmpdirname, 'foo', 'file'), 'w').close()

            observer.check()

            self.assertEqual(1, len(mock_function.mock_calls))

    def test_observer_signature_doesNotExists(self):
        observer = Observer()
        result = observer.get_path_signature('/blah')
        self.assertIsNone(result)

    def test_observer_signature_directory(self):
        observer = Observer()
        with tempfile.TemporaryDirectory() as tmpdirname:
            result = observer.get_path_signature(tmpdirname)
            self.assertIsNotNone(result)

    def test_observer_signature_file(self):
        observer = Observer()
        with tempfile.TemporaryDirectory() as tmpdirname:
            open(os.path.join(tmpdirname, 'file'), 'w').close()
            result = observer.get_path_signature(os.path.join(tmpdirname, 'file'))
            self.assertIsNotNone(result)

    def test_observer_signature_thread(self):
        observer = Observer()
        observer.start()
        observer.stop()

    def stest_observer_signature_loop(self):
        observer = Observer()

        runner = Runner(observer)
        runner.start()
        time.sleep(0.1)
        raise KeyboardInterrupt()
        runner.join()


class Runner(threading.Thread):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer

    def run(self):
        self.observer.loop()
