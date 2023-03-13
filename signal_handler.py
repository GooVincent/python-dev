import time
import signal
from threading import Event as ThreadEvent

class SignalHandler():
    """SignalHandler
    """
    def __init__(self, signalnum, handler, *args):
        self.signalnum = signalnum
        self.handler = handler
        self.args = args

    def _sig_handler(self, func, *args, signum=None, frame=None):
        """ sig_handler
            signum  and frame won't be used here, signal.signal handler requires for them

            args:
            func -- callback function, the params should pass as a list
            args -- callback function args including signum, frame from inner signal.signal handler
            signum -- as signal.signal handler require keyword-only param
            frame -- as signal.signal handler require keyword-only param
        """
        callback_func_real_args, _, _ = args
        func(callback_func_real_args)

    def register(self):
        from functools import partial
        format_sig_handler_cb = partial(self._sig_handler, self.handler, self.args)
        signal.signal(self.signalnum, format_sig_handler_cb)


def callback(args: tuple):
    event, *_ = args
    event.set()


def main():
    terminate_event = ThreadEvent()
    sig_handler = SignalHandler(signal.SIGTERM, callback, terminate_event)
    sig_handler.register()

    while not terminate_event.is_set():
        time.sleep(1)
        print('waiting for the signal')


if __name__ == '__main__':
    main()
