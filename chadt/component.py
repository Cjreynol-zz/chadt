from threading import Thread
from time import sleep

from chadt.chadt_exceptions import ComponentStoppingException, ComponentShuttingDownException
from chadt.component_status import ComponentStatus
from chadt.constants import THREAD_SLEEP_TIME


class Component:
    """Intended as a base class for threaded parts of the application.

    The expectation is that the sub-class will likely override the start 
    method, where they will use super to call this class' start with the 
    function intended to be repeated.

    The rest of the logic has to do with repeating the given function until 
    a call to stop or shutdown is made, with the semantics of what the 
    difference between them left up to the sub-class.

    """

    def __init__(self):
        self.status = ComponentStatus.STOPPED

    def start(self, thread_target):
        """Starts a new thread of execution using the given target function, 
        provided the Component is in a state to be restarted.
        """
        if self.status == ComponentStatus.STOPPED:
            self.status = ComponentStatus.RUNNING
            Thread(target = self.get_run_func(thread_target)).start()
        elif self.status == ComponentStatus.STOPPING:
            raise ComponentStoppingException()
        elif self.status == ComponentStatus.SHUTTING_DOWN or self.status == ComponentStatus.SHUT_DOWN:
            raise ComponentShuttingDownException()

    def get_run_func(self, target_func):
        """Handles wrapping the given function in the necessary logic for 
        repeating it until the Component's state is changed.
        """
        def f():
            while self.status == ComponentStatus.RUNNING:
                target_func()
                sleep(THREAD_SLEEP_TIME)
            if self.status == ComponentStatus.STOPPING:
                self.status = ComponentStatus.STOPPED
            elif self.status == ComponentStatus.SHUTTING_DOWN:
                self.status = ComponentStatus.SHUT_DOWN
        return f

    def stop(self):
        """Changes the state of the Component to signal the thread to stop
        repeating and enter a STOPPED state.
        """
        if self.status == ComponentStatus.RUNNING:
            self.status = ComponentStatus.STOPPING

    def shutdown(self):
        """Changes the state of the Component to signal the thread to stop
        repeating and enter a SHUT_DOWN state.
        """
        if self.status == ComponentStatus.RUNNING or self.status == ComponentStatus.STOPPING:
            self.status = ComponentStatus.SHUTTING_DOWN
        elif self.status == ComponentStatus.STOPPED:
            self.status = ComponentStatus.SHUT_DOWN
