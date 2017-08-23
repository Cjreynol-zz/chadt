from threading import Thread
from time import sleep

from chadt.chadt_exceptions import ComponentStoppingException, ComponentShuttingDownException
from chadt.component_status import ComponentStatus


class ChadtComponent:

    THREAD_SLEEP_TIME = 0.05
    
    def __init__(self):
        self.status = ComponentStatus.STOPPED

    def start(self, thread_target):
        if self.status == ComponentStatus.STOPPED:
            self.status = ComponentStatus.RUNNING
            Thread(target = self.get_run_func(thread_target)).start()
        elif self.status == ComponentStatus.STOPPING:
            raise ComponentStoppingException("Cannot be restarted yet.")
        elif self.status == ComponentStatus.SHUTTING_DOWN or self.status == ComponentStatus.SHUT_DOWN:
            raise ComponentShuttingDownException("Will not be able to be restarted.")

    def get_run_func(self, target_func):
        def f():
            while self.status == ComponentStatus.RUNNING:
                target_func()
                sleep(ChadtComponent.THREAD_SLEEP_TIME)
            if self.status == ComponentStatus.STOPPING:
                self.status = ComponentStatus.STOPPED
            elif self.status == ComponentStatus.SHUTTING_DOWN:
                self.status = ComponentStatus.SHUT_DOWN
        return f

    def stop(self):
        if self.status == ComponentStatus.RUNNING:
            self.status = ComponentStatus.STOPPING

    def shutdown(self):
        if self.status == ComponentStatus.RUNNING or self.status == ComponentStatus.STOPPING:
            self.status = ComponentStatus.SHUTTING_DOWN
        elif self.status == ComponentStatus.STOPPED:
            self.status = ComponentStatus.SHUT_DOWN
