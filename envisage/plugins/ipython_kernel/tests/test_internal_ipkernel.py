import contextlib
import gc
import logging
import os
import sys
import tempfile
import unittest

try:
    import ipykernel  # noqa: F401
except ImportError:
    ipykernel_available = False
else:
    ipykernel_available = True


if ipykernel_available:
    from ipykernel.iostream import IOPubThread
    from ipykernel.kernelapp import IPKernelApp
    import IPython.utils.io

    from envisage.plugins.ipython_kernel.internal_ipkernel import (
        InternalIPKernel)


# Machinery for catching logged messages in tests (both for testing
# the existence and content of those messages, and for hiding the
# logger output during the test run).

class ListHandler(logging.Handler):
    """
    Simple logging handler that stores all records in a list.

    Used by catch_logs below.
    """
    def __init__(self):
        logging.Handler.__init__(self)
        self.records = []

    def emit(self, record):
        self.records.append(record)


@contextlib.contextmanager
def catch_logs(logger_name, level=logging.WARNING):
    """
    Temporarily redirect logs for the given logger to a list.

    Also allows temporarily changing the level of that logger.
    """
    logger = logging.getLogger(logger_name)
    handler = ListHandler()
    old_propagate = logger.propagate
    old_level = logger.level

    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(level)
    try:
        yield handler.records
    finally:
        logger.setLevel(old_level)
        logger.propagate = old_propagate
        logger.removeHandler(handler)


@contextlib.contextmanager
def capture_stream(stream, callback=None):
    """
    Context manager to capture output to a particular stream.

    Capture all output written to the given stream. If the optional
    callback is provided, call it with the captured output (which
    will be a bytestring) when exiting the with block.

    Parameters
    ----------
    stream : Python stream
        For example, sys.__stdout__.
    callback : callable
        Callable of a single argument.
    """
    stream_fd = stream.fileno()

    with tempfile.TemporaryFile() as new_stream:
        old_stream_fd = os.dup(stream_fd)
        stream.flush()
        os.dup2(new_stream.fileno(), stream_fd)
        try:
            yield
        finally:
            stream.flush()
            os.dup2(old_stream_fd, stream_fd)
            os.close(old_stream_fd)

        new_stream.flush()
        new_stream.seek(0)
        captured = new_stream.read()

    if callback is not None:
        callback(captured)


@unittest.skipUnless(ipykernel_available,
                     "skipping tests that require the ipykernel package")
class TestInternalIPKernel(unittest.TestCase):

    def tearDown(self):
        IPKernelApp.clear_instance()

    def test_lifecycle(self):
        kernel = InternalIPKernel()
        self.assertIsNone(kernel.ipkernel)

        kernel.init_ipkernel(gui_backend=None)
        self.assertIsNotNone(kernel.ipkernel)
        self.assertIsInstance(kernel.ipkernel, IPKernelApp)

        kernel.new_qt_console()
        kernel.new_qt_console()
        self.assertEqual(len(kernel.consoles), 2)

        kernel.shutdown()
        self.assertIsNone(kernel.ipkernel)
        self.assertEqual(len(kernel.consoles), 0)

    def test_initial_namespace(self):
        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
        kernel.init_ipkernel(gui_backend=None)
        self.assertIn('x', kernel.namespace)
        self.assertEqual(kernel.namespace['x'], 42.1)
        kernel.shutdown()

    def test_shutdown_restores_output_streams(self):
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
        kernel.init_ipkernel(gui_backend=None)
        kernel.shutdown()

        self.assertIs(sys.stdout, original_stdout)
        self.assertIs(sys.stderr, original_stderr)

    def test_shutdown_closes_console_pipes(self):
        kernel = InternalIPKernel(initial_namespace=[('x', 42.1)])
        kernel.init_ipkernel(gui_backend=None)
        console = kernel.new_qt_console()
        self.assertFalse(console.stdout.closed)
        self.assertFalse(console.stderr.closed)
        kernel.shutdown()
        self.assertTrue(console.stdout.closed)
        self.assertTrue(console.stderr.closed)

    def test_io_pub_thread_stopped(self):
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        kernel.new_qt_console()
        kernel.new_qt_console()
        kernel.shutdown()

        io_pub_threads = [
            obj for obj in gc.get_objects()
            if isinstance(obj, IOPubThread)
        ]

        for thread in io_pub_threads:
            self.assertFalse(thread.thread.is_alive())

    def XXXtest_ctrl_c_message_suppressed(self):
        captured = []
        with capture_stream(sys.__stdout__, callback=captured.append):
            kernel = InternalIPKernel()
            kernel.init_ipkernel(gui_backend=None)
            kernel.shutdown()

        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertNotIn("Ctrl-C will not work", captured_stdout)

    def XXXtest_raw_print_logged(self):
        test_message = "norwegian blue"

        # Outside the context of the kernel, raw_print prints as expected.
        captured = []
        with capture_stream(sys.__stdout__, callback=captured.append):
            IPython.utils.io.raw_print(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

        # Again, with a running kernel.
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        captured = []
        log_catcher = catch_logs(
            "envisage.plugins.ipython_kernel", level=logging.INFO)

        try:
            with log_catcher as log_records:
                with capture_stream(sys.__stdout__, callback=captured.append):
                    IPython.utils.io.raw_print(test_message)
        finally:
            kernel.shutdown()

        # Check captured output (which should not contain the test message)
        # and the INFO-level log records (which should).
        messages = [
            record.getMessage() for record in log_records
            if record.levelno == logging.INFO
        ]
        test_message_found = any(
            test_message in message for message in messages)
        self.assertTrue(
            test_message_found,
            msg="raw_print messages were not found in the logs"
        )
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertNotIn(test_message, captured_stdout)

        # After shutdown, raw_print again prints to __stdout__.
        captured = []
        with capture_stream(sys.__stdout__, callback=captured.append):
            IPython.utils.io.raw_print(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

    def XXXtest_raw_print_err_logged(self):
        test_message = "your hovercraft is full of eels"

        # Outside the context of the kernel, raw_print_err prints as expected.
        captured = []
        with capture_stream(sys.__stderr__, callback=captured.append):
            IPython.utils.io.raw_print_err(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)

        # Again, with a running kernel.
        kernel = InternalIPKernel()
        kernel.init_ipkernel(gui_backend=None)
        captured = []
        log_catcher = catch_logs(
            "envisage.plugins.ipython_kernel", level=logging.WARNING)

        try:
            with log_catcher as log_records:
                with capture_stream(sys.__stderr__, callback=captured.append):
                    IPython.utils.io.raw_print_err(test_message)
        finally:
            kernel.shutdown()

        # Check captured output (which should not contain the test message)
        # and the INFO-level log records (which should).
        messages = [
            record.getMessage() for record in log_records
            if record.levelno == logging.WARNING
        ]
        test_message_found = any(
            test_message in message for message in messages)
        self.assertTrue(
            test_message_found,
            msg="raw_print_err messages were not found in the logs"
        )
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertNotIn(test_message, captured_stdout)

        # After shutdown, raw_print_err again prints to __stderr__.
        captured = []
        with capture_stream(sys.__stderr__, callback=captured.append):
            IPython.utils.io.raw_print_err(test_message)
        self.assertEqual(len(captured), 1)
        captured_stdout = captured[0].decode("utf-8")
        self.assertIn(test_message, captured_stdout)
